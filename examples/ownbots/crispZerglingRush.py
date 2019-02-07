import random
import time
import math

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2



class CrispZergRushBot(sc2.BotAI):
    
    def __init__(self):
        self.drone_counter_prior = 0
        self.drone_counter_after = 0
        self.extractor_started = False
        self.spawning_pool_started = False
        self.moved_workers_to_gas = False
        self.moved_workers_from_gas = False
        self.queeen_started = False
        self.mboost_started = False
        

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return self.known_enemy_structures
        else:
            return self.enemy_start_locations[0]
    
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

        enemy_natural = self.calculate_enemy_natural()
        own_natural = self.calculate_own_natural()

        if len(self.units(OVERLORD)) == 1:
            scout = self.units(OVERLORD)[0]
            if scout.is_idle:
                await self.do(scout.move(enemy_natural))

        if len(self.units(OVERLORD)) == 2:
            scout = self.units(OVERLORD)[1]
            if scout.is_idle:
                await self.do(scout.move(own_natural))
        

        for queen in self.units(QUEEN).idle:
            abilities = await self.get_available_abilities(queen)
            if AbilityId.EFFECT_INJECTLARVA in abilities:
                await self.do(queen(EFFECT_INJECTLARVA, hatchery))

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

            if not self.moved_workers_from_gas:
                self.moved_workers_from_gas = True
                for drone in self.workers:
                    m = self.state.mineral_field.closer_than(15, drone.position)
                    await self.do(drone.gather(m.random, queue=True)) ## for loop here until we have target drones all in minerals
        
        if self.supply_left < 2 and not self.already_pending(OVERLORD):
            if self.can_afford(OVERLORD) and larvae.exists:
                await self.do(larvae.random.train(OVERLORD))


        if self.units(SPAWNINGPOOL).ready.exists and self.mboost_started == True:
            if larvae.exists and self.can_afford(ZERGLING):
                await self.do(larvae.random.train(ZERGLING))

        if self.minerals > 350 and self.units(HATCHERY).amount < 2:
            await self.expand_now()

        # target = self.known_enemy_structures.random_or(self.enemy_start_locations[0]).position
        if self.units(ZERGLING).amount > 16: 
            for zl in self.units(ZERGLING).idle:
                await self.do(zl.attack(self.find_target(self.state)))

def main():
    sc2.run_game(sc2.maps.get("CatalystLE"), [
        Bot(Race.Zerg, CrispZergRushBot()),
        Computer(Race.Terran, Difficulty.Medium)
    ],  realtime=False, save_replay_as="./replays/{bot1}_vs_{bot2}_{map}_{time}.SC2Replay".format(bot1="CrispZergRushBot", bot2="DefaultTerranMedium", map="CatalystLE".replace(" ", ""), time=time.strftime("%H_%M_%j")))

if __name__ == '__main__':
    main()