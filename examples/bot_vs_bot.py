import sc2
import time
from sc2 import Race
from sc2.player import Bot

from zerg.zerg_rush import ZergRushBot
from ownbots.crispZerglingRush import CrispZergRushBot
from ownbots.refactor import refactorBot
from protoss.cannon_rush import CannonRushBot
from protoss.threebase_voidray import ThreebaseVoidrayBot
from protoss.warpgate_push import WarpGateBot
from terran.ramp_wall import RampWallBot
from terran.mass_reaper import MassReaperBot
from terran.proxy_rax import ProxyRaxBot
from terran.cyclone_push import CyclonePushBot


def main():
    sc2.run_game(sc2.maps.get("(2)DreamcatcherLE"), [
        Bot(Race.Zerg, refactorBot()),
        Bot(Race.Terran, CyclonePushBot())
    ], realtime=False, save_replay_as="./replays/{bot1}_vs_{bot2}_{map}_{time}.SC2Replay".format(bot1="refactor", bot2="ProxyRaxBot", map="DreamcatcherLE".replace(" ", ""), time=time.strftime("%H_%M_%j")))

if __name__ == '__main__':
    main()
