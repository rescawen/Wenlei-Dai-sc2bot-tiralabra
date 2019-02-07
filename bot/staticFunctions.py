    
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