import random
import time
import math

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit

class refactorBot(sc2.BotAI):
    
    # Global variables to keep track of certain things in the state of the game, this will give methods the condition to execute certain things

    def __init__(self):
        self.drone_counter_prior = 0
        self.drone_counter_after = 0
        self.extractor_started = False
        self.spawning_pool_started = False
        self.moved_workers_to_gas = False
        self.moved_workers_from_gas = False
        self.queeen_started = False
        self.mboost_started = False
        self.overlord_scout_order_count = 0
        self.workerCap = 24
        self.thirdBaseStarted = False
        
    # Find target is used to determine in which order should the army engage in battle

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
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

        hatchery = self.units(HATCHERY).ready.first
        larvae = self.units(LARVA)
        spawningpool = self.units(SPAWNINGPOOL).ready
        extractor = self.units(EXTRACTOR).ready


        # await self.on_unit_created(Unit)
        await self.injecting(hatchery)
        await self.trainOverlords(larvae)
        
        await self.naturalExpand()
        await self.thirdExpand()
        # await self.speedFinishedPush()
        await self.battle()
        await self.workerDistribution()
        

        if self.time < 180:
            await self.openingBuild(larvae, hatchery, extractor)
            await self.trainZerglings(larvae)
        
        if self.time > 180:
            await self.postPressureMacro(larvae)
        
    # Scouting for overlords in initial state of the game is only required do once, hence it is executed immediately when the unit is created

    async def on_unit_created(self, unit:Unit):
        enemy_natural = self.calculate_enemy_natural()
        own_natural = self.calculate_own_natural()
        if unit.type_id == OVERLORD:
            self.overlord_scout_order_count += 1
            await self.scouting(unit, enemy_natural, own_natural)

    # When a new base is created we calculate the theoretical maximum number of workers we want to have in each of the bases
    
    async def on_building_construction_complete(self, unit:Unit):
        if unit.type_id == HATCHERY:
            self.workerCap = self.units(HATCHERY).amount * 21
        print(self.workerCap)

    # The scouting algorithm 

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

    async def trainZerglings(self, larvae):
        if self.units(SPAWNINGPOOL).ready.exists and self.mboost_started == True:
            if larvae.exists and self.can_afford(ZERGLING):
                await self.do(larvae.random.train(ZERGLING))

    # async def speedFinishedPush(self):
    #     if self.units(ZERGLING).amount > 16: 
    #         for zl in self.units(ZERGLING).idle:
    #                 await self.do(zl.attack(self.find_target(self.state)))
    
    async def battle(self):
        actions = []
        if self.units(ZERGLING).amount > 0:
            if self.known_enemy_units.exists:
                for zl in self.units(ZERGLING):
                    actions.append(zl.attack(random.choice(self.known_enemy_units).position))
                await self.do_actions(actions)

    async def naturalExpand(self):
        if self.minerals > 350 and self.units(HATCHERY).amount < 2:
            await self.expand_now()

    async def thirdExpand(self):
        if self.minerals > 350 and self.units(HATCHERY).amount < 3 and self.units(DRONE).amount > 25 and self.already_pending(HATCHERY) == False:
            await self.expand_now()

    async def postPressureMacro(self, larvae):
        actions = []
        
        if larvae.exists and self.can_afford(DRONE) and (self.units(DRONE).amount + self.already_pending(DRONE)) < self.workerCap:
            actions.append(larvae.random.train(DRONE))

        if self.units(DRONE).amount > 29:
            if self.can_afford(EXTRACTOR):
                drone = self.workers.random
                target = self.state.vespene_geyser.closest_to(drone.position)
                actions.append(drone.build(EXTRACTOR, target))

        await self.do_actions(actions)

    async def workerDistribution(self):
        if self.units(HATCHERY).amount > 1:
            await self.distribute_workers()


def main():
    sc2.run_game(sc2.maps.get("(2)DreamcatcherLE"), [
        Bot(Race.Zerg, refactorBot()),
        Computer(Race.Terran, Difficulty.Easy)
    ],  realtime=False, save_replay_as="./replays/{bot1}_vs_{bot2}_{map}_{time}.SC2Replay".format(bot1="refactor", bot2="DefaultTerranHard", map="DreamcatcherLE".replace(" ", ""), time=time.strftime("%H_%M_%j")))

if __name__ == '__main__':
    main()