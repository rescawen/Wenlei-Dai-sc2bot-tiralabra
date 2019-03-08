import sc2
from sc2.constants import *

# naturalExpand and thirdExpand are only necessary for pressure opener build. 
# The reason why we don't have them in earlyGameBuildOrder is because if we do recover from early game chaos,
# we can still continue on our original gameplan later by continuing to expand. 
# So in conclusion I could have these lines of code in the earlyGameBuildOrder, but having them as general rule
# for looking at the game state takes into account more situations and we don't need to have same code twice.

async def naturalExpand(self, totalBaseCount):
    if self.minerals > 350 and totalBaseCount < 2:
        await self.expand_now()

async def thirdExpand(self, totalBaseCount):
    if self.minerals > 350 and totalBaseCount < 3 and self.units(DRONE).amount > 25 and self.already_pending(HATCHERY) == False:
        await self.expand_now()

async def lategameExpand(self, totalBaseCount):
    # As the resources from initial bases start to dry out, one needs to continuously expand outwards.
    # In a high level game of Starcraft these expansions locations are where much of contention takes place.

    if self.minerals > 500 and totalBaseCount < 9 and self.already_pending(HATCHERY) == False and self.units(DRONE).amount > 60:
        await self.expand_now()
