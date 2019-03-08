import random

import sc2
from sc2.constants import *

# In RTS games all units take up supply, which is a sort of antiresource. The maximum is 200 and each overlord provides 8. 
# One needs to produce them at a rate depending on ones production capacity until you hit the maximum
# Theoretically you might want a little more than the bare minimum because sometimes they die in battle in later stages 
# of the game and it is not good to be supply blocked. 

async def trainOverlords(self, larvae, actions):
    # The reason why we don't use the unitQueue for Overlords, is that it is 
    # putting 2 into queue when only 1 is necessary.
    # When we train it as soon as we need it, the second won't be trained 
    # because we are checking the already pending situation.
    if self.supply_left < 2 and not self.already_pending(OVERLORD):
        if larvae.exists and self.can_afford(OVERLORD):
            actions.append(larvae.random.train(OVERLORD))

async def trainOverlordsinBatch(self, actions):
    # Later in the game when production increases, it is necessary to make multiple overlords at once
    if self.units(OVERLORD).amount < 23 and self.supply_left < 12 and self.already_pending(OVERLORD) < 3:
        self.unitQueue.enqueue(OVERLORD)

# Zerglings and Mutalisks are a classic combination since the orignal Starcraft.
# They are the fastest units the zerg arsenal and fight well in synergy together.
# The reason why I chose these 2 units for the main army units, is due to their mineral and gas ratios. 
# The cost of the Mutalisks is 100 gas which relatively high, which means it will deplete all the gas coming in.
# However we still mine much more minerals than gas so the minerals are being used for zerglings, overlords and more bases etc.
            
async def trainZerglings(self, actions):
    if self.units(SPAWNINGPOOL).ready.exists and self.mboost_started == True:
        self.unitQueue.enqueue(ZERGLING)

async def trainMutalisks(self, actions):
    if self.units(SPIRE).ready.exists:
        self.unitQueue.enqueue(MUTALISK)