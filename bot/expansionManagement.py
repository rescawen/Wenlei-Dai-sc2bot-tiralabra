import sc2
from sc2.constants import *

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
