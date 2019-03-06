import random

import sc2
from sc2.constants import *

# In RTS games all units take up supply, which is a sort of antiresource. The maximum is 200 and each overlord provides 8. 
    # One needs to produce them at a rate depending on ones production capacity until you hit the maximum
    # Theoretically you might want a little more than the bare minimum because sometimes they die in battle in later stages 
    # of the game and it is not good to be supply blocked. 

async def trainOverlords(self, larvae, actions):
        if self.supply_left < 2 and not self.already_pending(OVERLORD):
            self.unitQueue.enqueue(OVERLORD)

async def trainOverlordsinBatch(self, larvae, actions):

    if self.units(OVERLORD).amount < 23 and self.supply_left < 12 and self.already_pending(OVERLORD) < 3:
        self.unitQueue.enqueue(OVERLORD)
            
    
async def trainZerglings(self, larvae, actions):
    if self.units(SPAWNINGPOOL).ready.exists and self.mboost_started == True:
        self.unitQueue.enqueue(ZERGLING)

async def trainMutalisks(self, larvae, actions):
    self.unitQueue.enqueue(MUTALISK)
    