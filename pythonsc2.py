import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer


class MyBot(sc2.BotAI):
    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("(glhf)")
           

run_game(maps.get("AcidPlantLE"), [
    Bot(Race.Zerg, MyBot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True)