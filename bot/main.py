import json
from pathlib import Path

import random
import time
import math

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.game_info import GameInfo

# from asdasd import find_target, battle_target, calculate_enemy_natural, calculate_own_natural

from bot.economyOpener import economyOpenerBuild



class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):

        self.drone_counter_prior = 0
        self.drone_counter_after = 0
        self.extractor_started = False
        self.spawning_pool_started = False
        self.moved_workers_to_gas = False
        self.moved_workers_from_gas = 0
        self.queeen_started = False
        self.mboost_started = False
        self.overlord_scout_order_count = 0
        self.workerCap = 24
        self.thirdBaseStarted = False
        self.lairStarted = False
        self.spireStarted = False
        self.evoChamberStarted = False
        self.groundUpgradeStarted = False
        self.airUpgradeStarted = False
        self.naturalBaseTag = 0
        
        
    # Find target is used to determine in which order should the army engage in battle

    def find_target(self, state):
        if self.known_enemy_units.filter(lambda u: not u.is_flying).exists:
            return random.choice(self.known_enemy_units.filter(lambda u: not u.is_flying))
        elif len(self.known_enemy_structures) > 0:
            return self.known_enemy_structures
        else:
            return self.enemy_start_locations[0]

    def battle_target(self):
        if self.known_enemy_units.exists:
            return random.choice(self.known_enemy_units).position
    
    # Calculating the location of the immediate expansion base called the natural expansion, this information is required for scouting patterns
    
    def calculate_enemy_natural(self) -> Point2:
        enemy_base = self.enemy_start_locations[0]
        best = None
        distance = math.inf
        for expansion in self.expansion_locations:
            temp = expansion.distance2_to(enemy_base)
            if temp < distance and temp > 0:
                distance = temp
                best = expansion
        return best

    def calculate_own_natural(self) -> Point2:
        own_base = self.start_location
        best = None
        distance = math.inf
        for expansion in self.expansion_locations:
            temp = expansion.distance2_to(own_base)
            if temp < distance and temp > 0:
                distance = temp
                best = expansion
        return best

    async def on_step(self, iteration):


        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")  

        if iteration == 1:
            self.mainBaseTag = self.townhalls.first.tag  
        
        hatchery = self.townhalls.first #fix this from crashing the game
        larvae = self.units(LARVA)
        # spawningpool = self.units(SPAWNINGPOOL).ready
        extractor = self.units(EXTRACTOR).ready
        totalBaseCount = self.townhalls.amount

        await self.on_unit_created(Unit)
        await self.injecting(hatchery)
        await self.trainOverlords(larvae)
        await self.naturalExpand(totalBaseCount)
        await self.thirdExpand(totalBaseCount)
        await self.lategameExpand(totalBaseCount)
        
        await self.workerDistribution(totalBaseCount)
        await self.continueUpgradingArmy()
        await self.returnWorkerstoMine()


        # await self.speedFinishedPush()

        # if self.evoChamberStarted == False:
        #     await self.buildEvochamber(totalBaseCount)

        if self.spireStarted == False:
            await self.buildSpire()
        
        if self.time < 150:
            await self.earlyGameDefense()

        ################### pressure
        if self.enemy_race == Race.Zerg or Race.Protoss:
            if self.time < 180:
                await self.pressureOpenerBuild(larvae, hatchery, extractor)
                await self.trainZerglings(larvae)
                await self.earlyGameBattle()
            
            if self.time > 180:
                await self.postPressureMacro(larvae, hatchery)

            if self.time > 400:
                await self.trainMutalisks(larvae)
                await self.trainZerglings(larvae)
                await self.trainOverlordsinBatch(larvae)
                await self.midGamePush()

        ######## macro

        if self.enemy_race == Race.Terran:
            if self.time < 185:
                await economyOpenerBuild(larvae, hatchery, extractor, totalBaseCount)
                # await self.trainZerglings(larvae)
                # await self.earlyGameBattle()
            
            if self.time > 185:
                await self.postPressureMacro(larvae, hatchery)
                await self.trainOverlordsinBatch(larvae)

            if self.time > 300:
                await self.trainMutalisks(larvae)
                await self.trainZerglings(larvae)
                await self.midGamePush()
        
            
        
    # Scouting for overlords in initial state of the game is only required do once, hence it is executed immediately when the unit is created

    async def on_unit_created(self, unit:Unit):
        enemy_natural = self.calculate_enemy_natural()
        own_natural = self.calculate_own_natural()
        if unit.type_id == OVERLORD:
            self.overlord_scout_order_count += 1
            await self.scouting(unit, enemy_natural, own_natural)

    # When a new base is created we calculate the theoretical maximum number of workers we want to have in each of the bases
    
    async def on_building_construction_complete(self, unit:Unit):
        hatchery1 = self.units.find_by_tag(self.mainBaseTag)
        hatchery2 = self.units.find_by_tag(self.naturalBaseTag)
        if unit.type_id == SPAWNINGPOOL:
            if self.can_afford(QUEEN) and hatchery1.noqueue and self.already_pending(QUEEN) < 3:
                await self.do(hatchery1.train(QUEEN))
            # for each hatchery in macro opener train queen
            if self.can_afford(QUEEN) and hatchery2.noqueue and self.already_pending(QUEEN) < 3:
                await self.do(hatchery2.train(QUEEN))
                self.naturalBaseTag = 1

        if unit.type_id == HATCHERY:

            if self.mainBaseTag != 0 and self.naturalBaseTag != 1:
                self.naturalBaseTag = unit.tag

            if self.can_afford(QUEEN):
                await self.do(unit.train(QUEEN))
            totalBaseCount = self.units(HATCHERY).amount + self.units(LAIR).amount + self.units(HIVE).amount
            if totalBaseCount < 4:
                self.workerCap =  totalBaseCount * 21
            else:
                self.workerCap = 66

        print(self.workerCap)
        
        if unit.type_id == EVOLUTIONCHAMBER:
            evochamber = self.units(EVOLUTIONCHAMBER).ready
            if self.can_afford(RESEARCH_ZERGMELEEWEAPONSLEVEL1):
                await self.do(evochamber.first(RESEARCH_ZERGMELEEWEAPONSLEVEL1))
                self.groundUpgradeStarted = True

        if unit.type_id == SPIRE:
            spire = self.units(SPIRE).ready
            if self.can_afford(RESEARCH_ZERGFLYERATTACKLEVEL1):
                await self.do(spire.first(RESEARCH_ZERGFLYERATTACKLEVEL1))
                self.airUpgradeStarted = True

    # The scouting algorithm 

    async def returnWorkerstoMine(self):
        actions = []
        for idle_worker in self.workers.idle:
            mf = self.state.mineral_field.closest_to(idle_worker)
            actions.append(idle_worker.gather(mf))
        await self.do_actions(actions)

    async def scouting(self, unit, enemy_natural, own_natural):
        
        # if self.overlord_scout_order_count == 1:
        #         await self.do(unit.move(enemy_natural))
        if self.overlord_scout_order_count == 1:
            positions = []
            for expansion in self.expansion_locations:
                if expansion == self.start_location or expansion == own_natural:
                    continue
                if expansion.distance_to(self.start_location) < 50 or expansion.distance_to(own_natural) < 50:
                    positions.append(expansion)
            for position in positions:
                await self.do(unit.move(position, True))
        
        if self.overlord_scout_order_count == 2:
            positions = []
            for expansion in self.expansion_locations:
                if expansion == self.start_location or expansion == own_natural:
                    continue
                if expansion.distance_to(self.start_location) < 60 or expansion.distance_to(own_natural) < 60:
                    positions.append(expansion)
            for position in positions:
                await self.do(unit.move(position, True))

        if self.overlord_scout_order_count == 3:
                await self.do(unit.move(own_natural))
        
        if self.overlord_scout_order_count == 4:
            positions = []
            for expansion in self.expansion_locations:
                if expansion == self.start_location or expansion == own_natural:
                    continue
                if expansion.distance_to(self.start_location) < 70 or expansion.distance_to(own_natural) < 70:
                    positions.append(expansion)
            for position in positions:
                await self.do(unit.move(position, True))

    # Injecting is the zerg race way of creating extra larvas which all units morphe from. This is basically getting the most amount of production capacity possible.

    async def injecting(self, hatchery):
        for queen in self.units(QUEEN).idle:
            abilities = await self.get_available_abilities(queen)
            if AbilityId.EFFECT_INJECTLARVA in abilities:
                await self.do(queen(EFFECT_INJECTLARVA, hatchery))

    # In RTS games all units take up supply, which is a sort of antiresource. The maximum is 200 and each overlord provides 8. 
    # One needs to produce them at a rate depending on ones production capacity until you hit the maximum
    # Theoretically you might want a little more than the bare minimum because sometimes they die in battle in later stages 
    # of the game and it is not good to be supply blocked. 

    async def trainOverlords(self, larvae):
        if self.supply_left < 2 and not self.already_pending(OVERLORD):
            if self.can_afford(OVERLORD) and larvae.exists:
                await self.do(larvae.random.train(OVERLORD))

    async def trainOverlordsinBatch(self, larvae):

        if self.units(OVERLORD).amount < 23 and self.supply_left < 12 and self.already_pending(OVERLORD) < 3:
            if self.can_afford(OVERLORD) and larvae.exists:
                await self.do(larvae.random.train(OVERLORD))
        
        # supplyNeeded = 200 - ((self.units(OVERLORD).amount * 8) + 18)

        # supplyPending = 0

        # while supplyNeeded >= supplyPending:
        #     if self.can_afford(OVERLORD) and larvae.exists:
        #         supplyPending += 8
        #         await self.do(larvae.random.train(OVERLORD))
        
    async def trainZerglings(self, larvae):
        if self.units(SPAWNINGPOOL).ready.exists and self.mboost_started == True:
            if larvae.exists and self.can_afford(ZERGLING):
                await self.do(larvae.random.train(ZERGLING))

    async def trainMutalisks(self, larvae):
        if larvae.exists and self.can_afford(MUTALISK):
                await self.do(larvae.random.train(MUTALISK))

    async def speedFinishedPush(self):
        if self.units(ZERGLING).amount > 16: 

            for zl in self.units(ZERGLING).idle:
                    await self.do(zl.attack(self.find_target(self.state)))
    
    # wait for units to pull up before before sending them in, this current thing is good in early game vs proxy rax for example but in later stage it will send units in 1 by 1
    
    async def earlyGameDefense(self):
        actions = []
        forces = self.units(ZERGLING) | self.units(DRONE)
        if forces.amount > 0:
            if self.known_enemy_units.amount > 1:
                for unit in forces:
                    actions.append(unit.attack(random.choice(self.known_enemy_units).position))
                await self.do_actions(actions)

    # self.known_enemy_units.filter(lambda u: not u.is_flying)
    # if not self.known_enemy_units.filter(lambda u: u.is_flying):

    async def earlyGameBattle(self):
        actions = []
        forces = self.units(ZERGLING) 
        if forces.amount > 0:
            if self.known_enemy_units.filter(lambda u: not u.is_flying).exists:
                for unit in forces:
                    actions.append(unit.attack(random.choice(self.known_enemy_units.filter(lambda u: not u.is_flying)).position))
                await self.do_actions(actions)

    # POTENTIAL TARGETFIRE WITH MUTAS, list of priority for the mutas?, separate for loops for zerglings and mutas, because zerglings cannot attack air
    # async def midLateGameBattle(self): 
    #     actions = []
    #     forces = self.units(ZERGLING) | self.units(MUTALISK)
    #     if self.units(MUTALISK).amount > 23:
    #         for unit in forces.idle:
    #             actions.append(unit.attack(self.find_target(self.state)))
    #         await self.do_actions(actions)    

    async def midGamePush(self):
        actions = []
        forces = self.units(ZERGLING) | self.units(MUTALISK)
        if self.units(MUTALISK).amount > 23:
            for unit in forces.idle:
                actions.append(unit.attack(self.find_target(self.state)))
            await self.do_actions(actions)    

    async def naturalExpand(self, totalBaseCount):
        if self.minerals > 350 and totalBaseCount < 2:
            await self.expand_now()

    async def thirdExpand(self, totalBaseCount):
        if self.minerals > 350 and totalBaseCount < 3 and self.units(DRONE).amount > 25 and self.already_pending(HATCHERY) == False:
            await self.expand_now()

    async def lategameExpand(self, totalBaseCount):

        pressure = 700
        economy = 500

        if self.minerals > economy and totalBaseCount < 9 and self.already_pending(HATCHERY) == False and self.units(DRONE).amount > 60:
            await self.expand_now()

    async def buildSpire(self):
        mainBase = self.units(LAIR).ready
        if mainBase.exists:
            if not (self.units(SPIRE).exists or self.already_pending(SPIRE)):
                if self.can_afford(SPIRE):
                    await self.build(SPIRE, near=mainBase.first)
                    self.spireStarted == True
    
    async def buildEvochamber(self, totalBaseCount):
        if self.units(LAIR).exists:
            mainBase = self.units(LAIR).ready
        else:
            mainBase = self.units(HATCHERY).ready
         # sometimes mainBase is lair and sometimes hatchery causing things to break
        if totalBaseCount > 2:
            if not (self.units(EVOLUTIONCHAMBER).exists or self.already_pending(EVOLUTIONCHAMBER)):
                if self.can_afford(EVOLUTIONCHAMBER):
                    await self.build(EVOLUTIONCHAMBER, near=mainBase.first)
                    self.evoChamberStarted == True

    async def continueUpgradingArmy(self):

        # start level1 upgrades if cannot afford immediately after evo chamber is finished

        if ZERGMELEEWEAPONSLEVEL1 in self.state.upgrades and self.already_pending_upgrade(ZERGMELEEWEAPONSLEVEL2) == False:
            evochamber = self.units(EVOLUTIONCHAMBER).ready
            if self.can_afford(RESEARCH_ZERGMELEEWEAPONSLEVEL2):
                await self.do(evochamber.first(RESEARCH_ZERGMELEEWEAPONSLEVEL2))

        if ZERGFLYERWEAPONSLEVEL1 in self.state.upgrades and self.already_pending_upgrade(ZERGFLYERWEAPONSLEVEL2) == False:
            spire = self.units(SPIRE).ready
            if self.can_afford(RESEARCH_ZERGFLYERATTACKLEVEL2):
                await self.do(spire.first(RESEARCH_ZERGFLYERATTACKLEVEL2))
                

    async def postPressureMacro(self, larvae, hatchery):
        actions = []
        
        if larvae.exists and self.can_afford(DRONE) and (self.units(DRONE).amount + self.already_pending(DRONE)) < self.workerCap:
            actions.append(larvae.random.train(DRONE))

        if self.units(DRONE).amount > 29:
            if self.can_afford(EXTRACTOR):
                drone = self.workers.random
                target = self.state.vespene_geyser.closest_to(drone.position)
                actions.append(drone.build(EXTRACTOR, target))

            mainBase = self.units.find_by_tag(self.mainBaseTag)

            if not self.units(LAIR).exists and mainBase.noqueue and self.already_pending(LAIR) == False:
                if self.can_afford(LAIR):
                    actions.append(mainBase.build(LAIR))

        await self.do_actions(actions)

    async def workerDistribution(self, totalBaseCount):
        if totalBaseCount > 1:
            await self.distribute_workers()


    async def pressureOpenerBuild(self, larvae, hatchery, extractor):
        if self.drone_counter_prior < 1:
            if self.can_afford(DRONE):
                self.drone_counter_prior += 1
                await self.do(larvae.random.train(DRONE))

        if not self.extractor_started:
            if self.can_afford(EXTRACTOR):
                drone = self.workers.random
                target = self.state.vespene_geyser.closest_to(drone.position)
                err = await self.do(drone.build(EXTRACTOR, target))
                if not err:
                    self.extractor_started = True

        elif not self.spawning_pool_started:
            if self.can_afford(SPAWNINGPOOL):
                for d in range(4, 15):
                    pos = hatchery.position.to2.towards(self.game_info.map_center, d)
                    if await self.can_place(SPAWNINGPOOL, pos):
                        drone = self.workers.closest_to(pos)
                        err = await self.do(drone.build(SPAWNINGPOOL, pos))
                        if not err:
                            self.spawning_pool_started = True
                            break

        elif not self.queeen_started and self.units(SPAWNINGPOOL).ready.exists:
            if self.can_afford(QUEEN):
                r = await self.do(hatchery.train(QUEEN))
                if not r:
                    self.queeen_started = True
        
        if self.drone_counter_after < 3 and extractor.exists:
            if self.can_afford(DRONE):
                self.drone_counter_after += 1
                await self.do(larvae.random.train(DRONE))

        if self.units(EXTRACTOR).ready.exists and not self.moved_workers_to_gas:
            self.moved_workers_to_gas = True
            extractor = self.units(EXTRACTOR).first
            for drone in self.workers.random_group_of(3):
                await self.do(drone.gather(extractor))

        if self.vespene >= 100:
            sp = self.units(SPAWNINGPOOL).ready
            if sp.exists and self.minerals >= 100 and not self.mboost_started:
                await self.do(sp.first(RESEARCH_ZERGLINGMETABOLICBOOST))
                self.mboost_started = True

            if self.moved_workers_from_gas == 0:
                self.moved_workers_from_gas += 1
                for drone in self.workers:
                    m = self.state.mineral_field.closer_than(10, drone.position)
                    await self.do(drone.gather(m.random, queue=True)) ## for loop here until we have target drones all in minerals

        if self.mboost_started == True and self.moved_workers_from_gas == 1 and self.vespene > 7:
            self.moved_workers_from_gas += 1
            for drone in self.workers:
                m = self.state.mineral_field.closer_than(10, drone.position)
                await self.do(drone.gather(m.random, queue=True))

    # async def economyOpenerBuild(self, larvae, hatchery, extractor, totalBaseCount):

    #     if self.drone_counter_prior < 2:
    #         if self.can_afford(DRONE) and larvae.exists:
    #             self.drone_counter_prior += 1
    #             await self.do(larvae.random.train(DRONE))
        
    #     if self.drone_counter_after < 5:
    #         if self.can_afford(DRONE) and larvae.exists:
    #             self.drone_counter_prior += 1
    #             await self.do(larvae.random.train(DRONE))

    #     if self.minerals > 300 and totalBaseCount < 2:
    #         await self.expand_now()

    #     if self.minerals > 300 and totalBaseCount < 3:
    #         await self.expand_now()
        
    #     if totalBaseCount == 3:
    #         if not self.spawning_pool_started:
    #             if self.can_afford(SPAWNINGPOOL):
    #                 for d in range(4, 15):
    #                     pos = hatchery.position.to2.towards(self.game_info.map_center, d)
    #                     if await self.can_place(SPAWNINGPOOL, pos):
    #                         drone = self.workers.closest_to(pos)
    #                         err = await self.do(drone.build(SPAWNINGPOOL, pos))
    #                         if not err:
    #                             self.spawning_pool_started = True
    #                             break

    #         elif not self.extractor_started:
    #             if self.can_afford(EXTRACTOR):
    #                 drone = self.workers.random
    #                 target = self.state.vespene_geyser.closest_to(drone.position)
    #                 err = await self.do(drone.build(EXTRACTOR, target))
    #                 if not err:
    #                     self.extractor_started = True
        
    #     if self.units(EXTRACTOR).ready.exists and not self.moved_workers_to_gas:
    #         self.moved_workers_to_gas = True
    #         extractor = self.units(EXTRACTOR).first
    #         for drone in self.workers.random_group_of(3):
    #             await self.do(drone.gather(extractor))

    #     if self.vespene >= 112:
    #         sp = self.units(SPAWNINGPOOL).ready
    #         if sp.exists and self.minerals >= 100 and not self.mboost_started:
    #             await self.do(sp.first(RESEARCH_ZERGLINGMETABOLICBOOST))
    #             self.mboost_started = True

