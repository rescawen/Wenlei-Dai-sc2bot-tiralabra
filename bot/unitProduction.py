import random

import sc2
from sc2.constants import *

# In RTS games all units take up supply, which is a sort of antiresource. The maximum is 200 and each overlord provides 8. 
    # One needs to produce them at a rate depending on ones production capacity until you hit the maximum
    # Theoretically you might want a little more than the bare minimum because sometimes they die in battle in later stages 
    # of the game and it is not good to be supply blocked. 

async def trainOverlords(self, larvae):
        if self.supply_left < 2 and not self.already_pending(OVERLORD):
            if self.can_afford(OVERLORD) and larvae.exists:
                await self.do(larvae.random.train(OVERLORD))

async def trainOverlordsinBatch(self, larvae):

    if self.units(OVERLORD).amount < 23 and self.supply_left < 12 and self.already_pending(OVERLORD) < 3:
        if self.can_afford(OVERLORD) and larvae.exists:
            await self.do(larvae.random.train(OVERLORD))
    
async def trainZerglings(self, larvae):
    if self.units(SPAWNINGPOOL).ready.exists and self.mboost_started == True:
        if larvae.exists and self.can_afford(ZERGLING):
            await self.do(larvae.random.train(ZERGLING))

async def trainMutalisks(self, larvae):
    if larvae.exists and self.can_afford(MUTALISK):
            await self.do(larvae.random.train(MUTALISK))