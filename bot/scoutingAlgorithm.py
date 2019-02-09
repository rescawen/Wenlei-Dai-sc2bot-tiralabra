import sc2
from sc2.constants import *

async def scouting(self, unit, enemy_natural, own_natural):
    
    # if self.overlord_scout_order_count == 1:
    #         await self.do(unit.move(enemy_natural))
    if self.overlord_scout_order_count == 1:
        positions = []
        for expansion in self.expansion_locations:
            if expansion == self.start_location or expansion == own_natural:
                continue
            if expansion.distance_to(self.start_location) < 50 or expansion.distance_to(own_natural) < 50:
                positions.append(expansion)
        for position in positions:
            await self.do(unit.move(position, True))
    
    if self.overlord_scout_order_count == 2:
        positions = []
        for expansion in self.expansion_locations:
            if expansion == self.start_location or expansion == own_natural:
                continue
            if expansion.distance_to(self.start_location) < 60 or expansion.distance_to(own_natural) < 60:
                positions.append(expansion)
        for position in positions:
            await self.do(unit.move(position, True))

    if self.overlord_scout_order_count == 3:
            await self.do(unit.move(own_natural))
    
    if self.overlord_scout_order_count == 4:
        positions = []
        for expansion in self.expansion_locations:
            if expansion == self.start_location or expansion == own_natural:
                continue
            if expansion.distance_to(self.start_location) < 70 or expansion.distance_to(own_natural) < 70:
                positions.append(expansion)
        for position in positions:
            await self.do(unit.move(position, True))