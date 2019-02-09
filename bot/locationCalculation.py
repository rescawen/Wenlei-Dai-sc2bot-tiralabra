import math

import sc2
from sc2.constants import *
from sc2.position import Point2

# Calculating the location of the immediate expansion base called the natural expansion, this information is required for scouting patterns

def calculate_enemy_natural(self) -> Point2:
    enemy_base = self.enemy_start_locations[0]
    best = None
    distance = math.inf
    for expansion in self.expansion_locations:
        temp = expansion.distance2_to(enemy_base)
        if temp < distance and temp > 0:
            distance = temp
            best = expansion
    return best

def calculate_own_natural(self) -> Point2:
    own_base = self.start_location
    best = None
    distance = math.inf
    for expansion in self.expansion_locations:
        temp = expansion.distance2_to(own_base)
        if temp < distance and temp > 0:
            distance = temp
            best = expansion
    return best