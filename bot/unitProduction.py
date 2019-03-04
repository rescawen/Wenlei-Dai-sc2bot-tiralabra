import random

import sc2
from sc2.constants import *

# In RTS games all units take up supply, which is a sort of antiresource. The maximum is 200 and each overlord provides 8. 
    # One needs to produce them at a rate depending on ones production capacity until you hit the maximum
    # Theoretically you might want a little more than the bare minimum because sometimes they die in battle in later stages 
    # of the game and it is not good to be supply blocked. 

async def trainOverlords(self, larvae, actions):
        if self.supply_left < 2 and not self.already_pending(OVERLORD):
            if self.can_afford(OVERLORD) and larvae.exists:
                actions.append(larvae.random.train(OVERLORD))

        await self.do_actions(actions)

async def trainOverlordsinBatch(self, larvae, actions):

    if self.units(OVERLORD).amount < 23 and self.supply_left < 12 and self.already_pending(OVERLORD) < 3:
        if self.can_afford(OVERLORD) and larvae.exists:
            actions.append(larvae.random.train(OVERLORD))
    
    await self.do_actions(actions)
    
async def trainZerglings(self, larvae, actions):
    if self.units(SPAWNINGPOOL).ready.exists and self.mboost_started == True:
        if larvae.exists and self.can_afford(ZERGLING):
            actions.append(larvae.random.train(ZERGLING))
    
    await self.do_actions(actions)

async def trainMutalisks(self, larvae, actions):
    if larvae.exists and self.can_afford(MUTALISK):
            actions.append(larvae.random.train(MUTALISK))
    
    await self.do_actions(actions)