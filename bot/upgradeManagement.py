import sc2
from sc2.constants import *

async def continueUpgradingArmy(self, actions):
    # start level1 upgrades if cannot afford immediately after evo chamber is finished

    if ZERGMELEEWEAPONSLEVEL1 in self.state.upgrades and self.already_pending_upgrade(ZERGMELEEWEAPONSLEVEL2) == False:
        evochamber = self.units(EVOLUTIONCHAMBER).ready
        if self.can_afford(RESEARCH_ZERGMELEEWEAPONSLEVEL2):
            actions.append(evochamber.first(RESEARCH_ZERGMELEEWEAPONSLEVEL2))

    if ZERGFLYERWEAPONSLEVEL1 in self.state.upgrades and self.already_pending_upgrade(ZERGFLYERWEAPONSLEVEL2) == False:
        spire = self.units(SPIRE).ready
        if self.can_afford(RESEARCH_ZERGFLYERATTACKLEVEL2):
            actions.append(spire.first(RESEARCH_ZERGFLYERATTACKLEVEL2))
    
    await self.do_actions(actions)
                
