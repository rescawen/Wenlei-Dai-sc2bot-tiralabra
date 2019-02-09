import sc2
from sc2.constants import *

# Injecting is the zerg race way of creating extra larvas which all units morphe from. This is basically getting the most amount of production capacity possible.

async def injecting(self, hatchery):
    for queen in self.units(QUEEN).idle:
        abilities = await self.get_available_abilities(queen)
        if AbilityId.EFFECT_INJECTLARVA in abilities:
            await self.do(queen(EFFECT_INJECTLARVA, hatchery))