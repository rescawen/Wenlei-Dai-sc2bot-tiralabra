import sc2
from sc2.constants import *

async def returnWorkerstoMine(self, actions):
    
        for idle_worker in self.workers.idle:
            mf = self.state.mineral_field.closest_to(idle_worker)
            actions.append(idle_worker.gather(mf))
        await self.do_actions(actions)

async def workerDistribution(self, totalBaseCount):
        if totalBaseCount > 1:
            await self.distribute_workers()