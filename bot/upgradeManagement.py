import sc2
from sc2.constants import *

# After evolution chamber and spire finished building in the on_building_construction_complete hook,
# we started upgrades in those buildings. Here we simply continue upgrading as soon as level 1 are ready
# if we can afford it. If not we simply upgrade when they are ready. The reason for focusing on only these
# upgrades is because they yield relatively higher value than the other upgrade which is armor. 

async def continueUpgradingArmy(self, actions):
    if ZERGMELEEWEAPONSLEVEL1 in self.state.upgrades and self.already_pending_upgrade(ZERGMELEEWEAPONSLEVEL2) == False:
        evochamber = self.units(EVOLUTIONCHAMBER).ready
        if self.can_afford(RESEARCH_ZERGMELEEWEAPONSLEVEL2):
            actions.append(evochamber.first(RESEARCH_ZERGMELEEWEAPONSLEVEL2))

    if ZERGFLYERWEAPONSLEVEL1 in self.state.upgrades and self.already_pending_upgrade(ZERGFLYERWEAPONSLEVEL2) == False:
        spire = self.units(SPIRE).ready
        if self.can_afford(RESEARCH_ZERGFLYERATTACKLEVEL2):
            actions.append(spire.first(RESEARCH_ZERGFLYERATTACKLEVEL2))
    
    await self.do_actions(actions)
                
