import math

import sc2
from sc2.constants import *
from sc2.position import Point2

# HUOM. The core of the following code was not written by me. It was given to me from blodir and I tweaked it a lot.
# However I do understand it and will attempt to explain it.

# Calculating the location of the immediate expansion base called the natural expansion
# This information is required for scouting patterns

# Both of the functions below are essentially the same. It takes the main base location (own or enemies) 
# and goes through the list of all possible known expansion locations and finds the one that is the closest.
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

# The commented line simply directly moving the unit to enemy natural, however it was not useful 
# in scouting proxy locations.

# We have a positions list which is all the spots which the overlord will be flying to.
# We choose these spots based on our potential 3rd/4rth/5th location expansions. 
# Then the overlord will essentially a cresdent shape trip that will potentially spot enemy proxies.

# I acknowledge this is not very good code practice to have the same code written multiple times, just so
# that I can make a bigger cresdent that later produced overlords can scout further into the map.
async def scouting(self, unit, enemy_natural, own_natural):
    actions = []

    # if self.overlord_scout_order_count == 1:
    #         actions.append(unit.move(enemy_natural))

    if self.overlord_scout_order_count == 1:
        positions = []
        for expansion in self.expansion_locations:
            if expansion == self.start_location or expansion == own_natural:
                continue
            if expansion.distance_to(self.start_location) < 50 or expansion.distance_to(own_natural) < 50:
                positions.append(expansion)
        for position in positions:
            actions.append(unit.move(position, True))
    
    if self.overlord_scout_order_count == 2:
        positions = []
        for expansion in self.expansion_locations:
            if expansion == self.start_location or expansion == own_natural:
                continue
            if expansion.distance_to(self.start_location) < 60 or expansion.distance_to(own_natural) < 60:
                positions.append(expansion)
        for position in positions:
            actions.append(unit.move(position, True))

    if self.overlord_scout_order_count == 3:
            actions.append(unit.move(own_natural))
    
    if self.overlord_scout_order_count == 4:
        positions = []
        for expansion in self.expansion_locations:
            if expansion == self.start_location or expansion == own_natural:
                continue
            if expansion.distance_to(self.start_location) < 70 or expansion.distance_to(own_natural) < 70:
                positions.append(expansion)
        for position in positions:
            actions.append(unit.move(position, True))
            
    await self.do_actions(actions)