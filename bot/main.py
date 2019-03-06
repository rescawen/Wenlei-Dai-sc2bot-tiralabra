import json
from pathlib import Path

import random
import time

import sc2
from sc2 import Race
from sc2.constants import *
from sc2.unit import Unit

from bot.openingBuildOrder import economyOpenerBuild, pressureOpenerBuild
from bot.scoutingAlgorithm import scouting
from bot.locationCalculation import calculate_enemy_natural, calculate_own_natural
from bot.battleAlgorithm import find_target
from bot.workerManagement import workerDistribution, returnWorkerstoMine
from bot.unitProduction import trainOverlords, trainOverlordsinBatch, trainMutalisks, trainZerglings
from bot.expansionManagement import naturalExpand, thirdExpand, lategameExpand
from bot.structureProduction import buildSpire, buildEvochamber
from bot.queenManagement import injecting
from bot.upgradeManagement import continueUpgradingArmy

from bot.dataStructures.priorityQueue import PriorityQueue


class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):
        # Own variables for game state, used to keep track of important information or triggers for certain functions
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
        self.unitQueue = PriorityQueue()
        
    # Everything happens inside the on_step function
    async def on_step(self, iteration):

        actions = []

        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")  

        if iteration == 1:
            self.mainBaseTag = self.townhalls.first.tag 
        
        hatchery = self.townhalls.first #fix this from crashing the game
        larvae = self.units(LARVA)
        extractor = self.units(EXTRACTOR).ready
        totalBaseCount = self.townhalls.amount

        await self.produceUnitsFromQueue(larvae, actions, self.unitQueue)

        await injecting(self, hatchery, actions)
        await trainOverlords(self, larvae, actions)
        await naturalExpand(self, totalBaseCount)
        await thirdExpand(self, totalBaseCount)
        await lategameExpand(self, totalBaseCount)
        await continueUpgradingArmy(self, actions)
        await returnWorkerstoMine(self, actions)
        await workerDistribution(self, totalBaseCount)

        # await self.speedFinishedPush()

        # if self.evoChamberStarted == False:
        #     await buildEvochamber(self, totalBaseCount)

        if self.spireStarted == False:
            await buildSpire(self)
        
        if self.time < 150:
            await self.earlyGameDefense(actions)

        # pressureOpenerBuild

        # if self.enemy_race == Race.Zerg or Race.Protoss or Race.Terran: just a reminder of how to pick opener based on opponents race

        #     if self.time < 180:
        #         await self.pressureOpenerBuild(larvae, hatchery, extractor)
        #         await self.trainZerglings(larvae)
        #         await self.earlyGameBattle()
    
        #     if self.time > 180:
        #         await self.midGameMacro(larvae, hatchery)

        #     if self.time > 400:
        #         await self.trainMutalisks(larvae)
        #         await self.trainZerglings(larvae)
        #         await self.trainOverlordsinBatch(larvae)
        #         await self.midGamePush()

        # economyOpenerBuild 
        
        if self.time < 185:
            await economyOpenerBuild(self, larvae, hatchery, extractor, totalBaseCount, actions)

        if self.time > 185:
            await self.midGameMacro(larvae, hatchery, actions)
            await trainOverlordsinBatch(self, larvae, actions)
            
                
        if self.time > 300:

            # if resources are high prioritize making army
            # if resources are low put in a few drones
            await trainMutalisks(self, larvae, actions)
            await trainZerglings(self, larvae, actions)
            await self.midGamePush(actions)
        
        
    # Scouting for overlords in initial state of the game is only required do once, hence it is executed immediately when the unit is created

    async def on_unit_created(self, unit:Unit):
        enemy_natural = calculate_enemy_natural(self)
        own_natural = calculate_own_natural(self)
        if unit.type_id == OVERLORD:
            self.overlord_scout_order_count += 1
            await scouting(self, unit, enemy_natural, own_natural)

    # When a new base is created we calculate the theoretical maximum number of workers we want to have in each of the bases
    
    async def on_building_construction_complete(self, unit:Unit):
        actions = []

        hatchery1 = self.units.find_by_tag(self.mainBaseTag)
        hatchery2 = self.units.find_by_tag(self.naturalBaseTag)

        if unit.type_id == SPAWNINGPOOL:
            if self.can_afford(QUEEN) and hatchery1.noqueue and self.already_pending(QUEEN) < 3:
                actions.append(hatchery1.train(QUEEN))
            # for each hatchery in macro opener train queen
            if self.can_afford(QUEEN) and hatchery2.noqueue and self.already_pending(QUEEN) < 3:
                actions.append(hatchery2.train(QUEEN))
                self.naturalBaseTag = 1

        if unit.type_id == HATCHERY:
            if self.mainBaseTag != 0 and self.naturalBaseTag != 1:
                self.naturalBaseTag = unit.tag
            if self.can_afford(QUEEN):
                actions.append(unit.train(QUEEN))
            totalBaseCount = self.units(HATCHERY).amount + self.units(LAIR).amount + self.units(HIVE).amount
            if totalBaseCount < 4:
                self.workerCap =  totalBaseCount * 21
            else:
                self.workerCap = 66
        
        if unit.type_id == EVOLUTIONCHAMBER:
            evochamber = self.units(EVOLUTIONCHAMBER).ready
            if self.can_afford(RESEARCH_ZERGMELEEWEAPONSLEVEL1):
                actions.append(evochamber.first(RESEARCH_ZERGMELEEWEAPONSLEVEL1))
                self.groundUpgradeStarted = True

        if unit.type_id == SPIRE:
            spire = self.units(SPIRE).ready
            if self.can_afford(RESEARCH_ZERGFLYERATTACKLEVEL1):
                actions.append(spire.first(RESEARCH_ZERGFLYERATTACKLEVEL1))
                self.airUpgradeStarted = True
        
        await self.do_actions(actions)

    async def speedFinishedPush(self, actions): #refactor this
        if self.units(ZERGLING).amount > 16: 
            for zl in self.units(ZERGLING).idle:
                await self.do(zl.attack(find_target(self, self.state)))
    
    # wait for units to pull up before before sending them in, this current thing is good in early game vs proxy rax for example but in later stage it will send units in 1 by 1
    
    async def earlyGameDefense(self, actions):
        forces = self.units(ZERGLING) | self.units(DRONE)
        if forces.amount > 0:
            if self.known_enemy_units.amount > 1:
                for unit in forces:
                    actions.append(unit.attack(random.choice(self.known_enemy_units).position))
        
        await self.do_actions(actions)

    async def earlyGameBattle(self, actions):
        forces = self.units(ZERGLING) 
        if forces.amount > 0:
            if self.known_enemy_units.filter(lambda u: not u.is_flying).exists:
                for unit in forces:
                    actions.append(unit.attack(random.choice(self.known_enemy_units.filter(lambda u: not u.is_flying)).position))
        
        await self.do_actions(actions) 

    async def midGamePush(self, actions):
        forces = self.units(ZERGLING) | self.units(MUTALISK)
        if self.units(MUTALISK).amount > 23:
            for unit in forces.idle:
                actions.append(unit.attack(find_target(self, self.state)))
            await self.do_actions(actions)    

    async def midGameMacro(self, larvae, hatchery, actions):
        if (self.units(DRONE).amount + self.already_pending(DRONE)) < self.workerCap:
            self.unitQueue.enqueue(DRONE)

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

    async def produceUnitsFromQueue(self, larvae, actions, unitQueue: PriorityQueue):
        for unit in unitQueue:
            if larvae.exists and self.can_afford(unit):
                actions.append(larvae.random.train(unitQueue.dequeue()))
            else:
                break

        await self.do_actions(actions)