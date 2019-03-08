import sc2
from sc2.constants import *

# Due to the nature of async, is there not a smarter way to build tech buildings? 

async def buildSpire(self):
    mainBase = self.units(LAIR).ready
    if mainBase.exists:
        if not (self.units(SPIRE).exists or self.already_pending(SPIRE)):
            if self.can_afford(SPIRE):
                await self.build(SPIRE, near=mainBase.first)
                self.spireStarted == True

async def buildEvochamber(self, totalBaseCount):
    if self.units(LAIR).exists:
        mainBase = self.units(LAIR).ready
    else:
        mainBase = self.units(HATCHERY).ready
    # sometimes mainBase is lair and sometimes hatchery causing things to break
    if totalBaseCount > 2:
        if not (self.units(EVOLUTIONCHAMBER).exists or self.already_pending(EVOLUTIONCHAMBER)):
            if self.can_afford(EVOLUTIONCHAMBER):
                await self.build(EVOLUTIONCHAMBER, near=mainBase.first)
                self.evoChamberStarted == True