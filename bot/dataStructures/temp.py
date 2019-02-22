if larvae.exists and self.can_afford(DRONE) and (self.units(DRONE).amount + self.already_pending(DRONE)) < self.workerCap:
            actions.append(larvae.random.train(DRONE))