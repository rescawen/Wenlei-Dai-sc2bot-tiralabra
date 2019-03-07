import random

import sc2
from sc2.constants import *

async def midGameMacro(self, hatchery, actions):
        if (self.units(DRONE).amount + self.already_pending(DRONE)) < self.workerCap:
            self.unitQueue.enqueue(DRONE)

        if self.units(DRONE).amount > 29:
            if self.can_afford(EXTRACTOR):
                drone = self.workers.random
                target = self.state.vespene_geyser.closest_to(drone.position)
                actions.append(drone.build(EXTRACTOR, target))

            mainBase = self.units.find_by_tag(self.mainBaseTag)
            if not self.units(LAIR).exists and mainBase.noqueue and self.already_pending(LAIR) == False:
                if self.can_afford(LAIR):
                    actions.append(mainBase.build(LAIR))

        await self.do_actions(actions)