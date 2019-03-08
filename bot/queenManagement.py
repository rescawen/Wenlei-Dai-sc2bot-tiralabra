import sc2
from sc2.constants import *

# Injecting is the zerg race way of creating extra larvas which all units morphe from. 
# This is routine job for getting the most amount of production capacity as possible.
# Queens have other abilities as well, which I did not have time to implement.
# This is the reason why it technically deserves another file because the implementation
# of creep spreading and healing much more complex. 

async def injecting(self, hatchery, actions):
    for queen in self.units(QUEEN).idle:
        abilities = await self.get_available_abilities(queen)
        if AbilityId.EFFECT_INJECTLARVA in abilities:
            actions.append(queen(EFFECT_INJECTLARVA, hatchery))

    await self.do_actions(actions)