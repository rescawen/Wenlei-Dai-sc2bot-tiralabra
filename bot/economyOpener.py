async def economyOpenerBuild(self, larvae, hatchery, extractor, totalBaseCount):

        if self.drone_counter_prior < 2:
            if self.can_afford(DRONE) and larvae.exists:
                self.drone_counter_prior += 1
                await self.do(larvae.random.train(DRONE))
        
        if self.drone_counter_after < 5:
            if self.can_afford(DRONE) and larvae.exists:
                self.drone_counter_prior += 1
                await self.do(larvae.random.train(DRONE))

        if self.minerals > 300 and totalBaseCount < 2:
            await self.expand_now()

        if self.minerals > 300 and totalBaseCount < 3:
            await self.expand_now()
        
        if totalBaseCount == 3:
            if not self.spawning_pool_started:
                if self.can_afford(SPAWNINGPOOL):
                    for d in range(4, 15):
                        pos = hatchery.position.to2.towards(self.game_info.map_center, d)
                        if await self.can_place(SPAWNINGPOOL, pos):
                            drone = self.workers.closest_to(pos)
                            err = await self.do(drone.build(SPAWNINGPOOL, pos))
                            if not err:
                                self.spawning_pool_started = True
                                break

            elif not self.extractor_started:
                if self.can_afford(EXTRACTOR):
                    drone = self.workers.random
                    target = self.state.vespene_geyser.closest_to(drone.position)
                    err = await self.do(drone.build(EXTRACTOR, target))
                    if not err:
                        self.extractor_started = True
        
        if self.units(EXTRACTOR).ready.exists and not self.moved_workers_to_gas:
            self.moved_workers_to_gas = True
            extractor = self.units(EXTRACTOR).first
            for drone in self.workers.random_group_of(3):
                await self.do(drone.gather(extractor))

        if self.vespene >= 112:
            sp = self.units(SPAWNINGPOOL).ready
            if sp.exists and self.minerals >= 100 and not self.mboost_started:
                await self.do(sp.first(RESEARCH_ZERGLINGMETABOLICBOOST))
                self.mboost_started = True