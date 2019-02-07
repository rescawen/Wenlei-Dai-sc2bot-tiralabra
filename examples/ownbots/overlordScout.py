import random
import time
import math

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit

class overlordScoutBot(sc2.BotAI):

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
    
    
    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("(glhf)")

    async def on_unit_created(self, unit:Unit):
        enemy_natural = self.calculate_enemy_natural()
        if unit.type_id == OVERLORD:
            self.overlord_scout_order_count += 1
            await self.scouting(unit, enemy_natural)

    async def scouting(self, unit, enemy_natural):
        
        if self.overlord_scout_order_count == 1:
                await self.do(unit.move(enemy_natural))

def main():
    sc2.run_game(sc2.maps.get("(2)CatalystLE"), [
        Bot(Race.Zerg, overlordScoutBot()),
        Computer(Race.Terran, Difficulty.Medium)
    ], realtime=False, save_replay_as="ZvT.SC2Replay")

if __name__ == '__main__':
    main()