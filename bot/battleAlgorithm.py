import random

import sc2
from sc2.constants import *

# Find target is used to determine in which order should the army engage in battle

def find_target(self, state):
    if self.known_enemy_units.filter(lambda u: not u.is_flying).exists:
        return random.choice(self.known_enemy_units.filter(lambda u: not u.is_flying))
    elif len(self.known_enemy_structures) > 0:
        return self.known_enemy_structures
    else:
        return self.enemy_start_locations[0]

def battle_target(self):
    if self.known_enemy_units.exists:
        return random.choice(self.known_enemy_units).position

async def earlyGameDefense(self, actions):
        forces = self.units(ZERGLING) | self.units(DRONE)
        if forces.amount > 0:
            if self.known_enemy_units.amount > 1:
                for unit in forces:
                    actions.append(unit.attack(random.choice(self.known_enemy_units).position))
        
        await self.do_actions(actions)

async def earlyGameBattle(self, actions):
        forces = self.units(ZERGLING) 
        if forces.amount > 0:
            if self.known_enemy_units.filter(lambda u: not u.is_flying).exists:
                for unit in forces:
                    actions.append(unit.attack(random.choice(self.known_enemy_units.filter(lambda u: not u.is_flying)).position))
        
        await self.do_actions(actions) 

async def speedFinishedPush(self, actions):
        if self.units(ZERGLING).amount > 16: 
            for zl in self.units(ZERGLING).idle:
                actions.append(zl.attack(find_target(self, self.state)))
        
        await self.do_actions(actions)

async def midGamePush(self, actions):
        forces = self.units(ZERGLING) | self.units(MUTALISK)
        if self.units(MUTALISK).amount > 23:
            for unit in forces.idle:
                actions.append(unit.attack(find_target(self, self.state)))
            await self.do_actions(actions)    