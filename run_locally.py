import json
import time

from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

from bot import MyBot
from examples.ownbots.workerRush import WorkerRushBot
from examples.ownbots.overlordScout import overlordScoutBot
from examples.terran.proxy_rax import ProxyRaxBot

def main():
    with open("botinfo.json") as f:
        info = json.load(f)

    race = Race[info["race"]]

    run_game(maps.get("(2)DreamCatcherLE"), [
        Bot(race, MyBot()),
        # Bot(Race.Terran, ProxyRaxBot())
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False, step_time_limit=2.0, game_time_limit=(60*20), save_replay_as="./replays/{bot1}_vs_{bot2}_{map}_{time}.SC2Replay".format(bot1="MyBot", bot2="DefaultRandomHard", map="DreamcatcherLE".replace(" ", ""), time=time.strftime("%H_%M_%j")))

if __name__ == '__main__':
    main()
