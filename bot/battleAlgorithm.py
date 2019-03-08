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

# The following earlyGameDefence/Battle are just dealing with different types of early game rushes. I couldn't come up with a better 
# naming scheme so that is why they might sound non arbitrary. 

async def earlyGameDefense(self, actions):
    # Deals with earliest rushes which come directly to my base and I need to pull workers to defend, used in combination returnWorkersToMine
    forces = self.units(ZERGLING) | self.units(DRONE)
    if forces.amount > 0:
        if self.known_enemy_units.amount > 1:
            for unit in forces:
                actions.append(unit.attack(random.choice(self.known_enemy_units).position))
    
    await self.do_actions(actions)

async def earlyGameBattle(self, actions):
    # Deals with rushes that build buildings outside my immediate vision or directly in my base. 
    # The key to defending is using overlords to spot those "proxy buildings" and then immediately going after them
    forces = self.units(ZERGLING) 
    if forces.amount > 0:
        if self.known_enemy_units.filter(lambda u: not u.is_flying).exists:
            for unit in forces:
                actions.append(unit.attack(random.choice(self.known_enemy_units.filter(lambda u: not u.is_flying)).position))
    
    await self.do_actions(actions) 

# The following the functions just look at the game state that we have enough units for a specific timing attack.
    
async def speedFinishedPush(self, actions):
    # This is used for the pressure opener where we coincide this pool of 16 zerglings once their 
    # speed upgrade finishes for an attack
    if self.units(ZERGLING).amount > 16: 
        for zl in self.units(ZERGLING).idle:
            actions.append(zl.attack(find_target(self, self.state)))
    
    await self.do_actions(actions)

async def mutaLingPush(self, actions):
    # Due to the fundamentals of SC2 economy, one only starts taking full advantage of 3 base which when 
    # one reaches relative peak production. Once you hit around 160 total supply it means you have taken 
    # full advantage of your economy which means it is a good time to attack. 
    forces = self.units(ZERGLING) | self.units(MUTALISK)
    if self.units(MUTALISK).amount > 23:
        for unit in forces.idle:
            actions.append(unit.attack(find_target(self, self.state)))
    
    await self.do_actions(actions)    