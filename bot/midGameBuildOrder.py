import random

import sc2
from sc2.constants import *

# This is not strictly speaking build order but general rules to follow once one exits the specific openers
# in the early game phase. 

async def midGameMacro(self, hatchery, actions):
    # Making sure that we don't overmake drones to theoretical optimal limit
    if (self.units(DRONE).amount + self.already_pending(DRONE)) < self.workerCap:
        self.unitQueue.enqueue(DRONE)

    # Making sure we maximize mineral income before starting to invest in technology, more advanced units that require gas
    if self.units(DRONE).amount > 29:
        if self.can_afford(EXTRACTOR):
            drone = self.workers.random
            target = self.state.vespene_geyser.closest_to(drone.position)
            actions.append(drone.build(EXTRACTOR, target))

        mainBase = self.units.find_by_tag(self.mainBaseTag)
        # Teching up to unlock more tech
        if not self.units(LAIR).exists and mainBase.noqueue and self.already_pending(LAIR) == False:
            if self.can_afford(LAIR):
                actions.append(mainBase.build(LAIR))

    await self.do_actions(actions)