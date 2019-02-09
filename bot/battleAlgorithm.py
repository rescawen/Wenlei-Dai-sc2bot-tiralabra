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