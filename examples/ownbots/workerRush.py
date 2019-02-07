import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer

class WorkerRushBot(sc2.BotAI):
    
    
    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("(glhf)")

        actions = []
        for worker in self.workers:
            actions.append(worker.attack(self.enemy_start_locations[0]))
        await self.do_actions(actions)


def main():
    sc2.run_game(sc2.maps.get("(2)CatalystLE"), [
        Bot(Race.Zerg, WorkerRushBot()),
        Computer(Race.Terran, Difficulty.Medium)
    ], realtime=False, save_replay_as="ZvT.SC2Replay")

if __name__ == '__main__':
    main()