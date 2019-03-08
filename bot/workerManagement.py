import sc2
from sc2.constants import *

# In some situations when early attacks come in and one needs to use drones for defence. 
# Without returnWorkertoMine the workers would simply go idle after the fight if they survive it. 
# This works together with earlyGameDefence in battleAlgorithm.

async def returnWorkerstoMine(self, actions):
    for idle_worker in self.workers.idle:
        mf = self.state.mineral_field.closest_to(idle_worker)
        actions.append(idle_worker.gather(mf))
    await self.do_actions(actions)

async def workerDistribution(self, totalBaseCount):
    # This distribute workers seems very trivial, so the reason why do not distribute workers
    # from the start of the game is that it would mess up the earlyGameBuildOrders.

    if totalBaseCount > 1:
        await self.distribute_workers()