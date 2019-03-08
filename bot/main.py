import json
from pathlib import Path

import random
import time

import sc2
from sc2 import Race
from sc2.constants import *
from sc2.unit import Unit

from bot.earlyGameBuildOrder import economyOpenerBuild, pressureOpenerBuild
from bot.midGameBuildOrder import midGameMacro
from bot.scoutingAlgorithm import calculate_enemy_natural, calculate_own_natural, scouting
from bot.battleAlgorithm import find_target, earlyGameDefense, earlyGameBattle, speedFinishedPush, mutaLingPush
from bot.workerManagement import workerDistribution, returnWorkerstoMine
from bot.unitProduction import trainOverlords, trainOverlordsinBatch, trainMutalisks, trainZerglings
from bot.expansionManagement import naturalExpand, thirdExpand, lategameExpand
from bot.structureProduction import buildSpire, buildEvochamber
from bot.queenManagement import injecting
from bot.upgradeManagement import continueUpgradingArmy

from bot.dataStructures.priorityQueue import PriorityQueue


class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):
        # Own variables for game state, used to keep track of important information or triggers for certain functions
        self.drone_counter_prior = 0
        self.drone_counter_after = 0
        self.extractor_started = False
        self.spawning_pool_started = False
        self.moved_workers_to_gas = False
        self.moved_workers_from_gas = 0
        self.queeen_started = False
        self.mboost_started = False
        self.overlord_scout_order_count = 0 
        self.workerCap = 24 #Worker count depends on how many bases one has and should be capped because too many would be inefficient
        self.thirdBaseStarted = False
        self.lairStarted = False
        self.spireStarted = False
        self.evoChamberStarted = False
        self.groundUpgradeStarted = False
        self.airUpgradeStarted = False
        self.naturalBaseTag = 0
        self.unitQueue = PriorityQueue()
        
    # Everything happens inside the on_step function
    async def on_step(self, iteration):

        actions = []

        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")  

        if iteration == 1:
            self.mainBaseTag = self.townhalls.first.tag 
        
        hatchery = self.townhalls.first #game crashes if starting base dies.
        larvae = self.units(LARVA)
        totalBaseCount = self.townhalls.amount

        # This list of functions we want to continuously keep doing or check to do
        await self.produceUnitsFromQueue(larvae, actions, self.unitQueue)
        await returnWorkerstoMine(self, actions)
        await workerDistribution(self, totalBaseCount)
        await injecting(self, hatchery, actions)
        await trainOverlords(self, larvae, actions)
        await naturalExpand(self, totalBaseCount) 
        await thirdExpand(self, totalBaseCount)
        await lategameExpand(self, totalBaseCount)
        await continueUpgradingArmy(self, actions)

        # Defending against a very specific early game all in in the bot tournament, versus default bots useless.
        if self.time < 150:
            await earlyGameDefense(self, actions)

        # PRESSURE OPENER BUILD comment and uncomment the until L#101 if economy opener is active 
        # if self.time < 180:
        #     await pressureOpenerBuild(self, larvae, hatchery, actions)
        #     await trainZerglings(self, actions)
        #     await earlyGameBattle(self, actions)
        #     await speedFinishedPush(self, actions)

        # if self.time > 180:
        #     await midGameMacro(self, hatchery, actions)

        # if self.time > 320: 
        #     if self.evoChamberStarted == False:
        #         await buildEvochamber(self, totalBaseCount)
        #     if self.spireStarted == False: #### do this in economy as well
        #         await buildSpire(self)

        # if self.time > 400:
        #     await trainMutalisks(self, actions)
        #     await trainZerglings(self, actions)
        #     await trainOverlordsinBatch(self, actions)
        #     await mutaLingPush(self, actions)

        # ECONOMY OPENER BUILD comment and uncomment the until L#120 if pressure opener is active 
        if self.time < 185:
            await economyOpenerBuild(self, larvae, hatchery, totalBaseCount, actions)

        if self.time > 185:
            await midGameMacro(self, hatchery, actions)
            await trainOverlordsinBatch(self, actions)

        if self.time > 250: 
            if self.evoChamberStarted == False:
                await buildEvochamber(self, totalBaseCount)
            if self.spireStarted == False: #### do this in economy as well
                await buildSpire(self)
                
        if self.time > 300:
            await trainMutalisks(self, actions)
            await trainZerglings(self, actions)
            await mutaLingPush(self, actions)
        
    # Scouting for overlords in initial state of the game is only required do once, hence it is executed immediately when the unit is created
    async def on_unit_created(self, unit:Unit):
        enemy_natural = calculate_enemy_natural(self)
        own_natural = calculate_own_natural(self)
        if unit.type_id == OVERLORD:
            self.overlord_scout_order_count += 1
            await scouting(self, unit, enemy_natural, own_natural)

    async def on_building_construction_complete(self, unit:Unit):
        actions = []
        if unit.type_id == SPAWNINGPOOL:
            # Sometimes spawning pool might finish after the hatcheries, in our case the economy opener has this situation.
            # Most of the time there is always resources to build the queens once they do............. continue
            hatchery1 = self.units.find_by_tag(self.mainBaseTag)
            hatchery2 = self.units.find_by_tag(self.naturalBaseTag)
            if self.can_afford(QUEEN) and hatchery1.noqueue and self.already_pending(QUEEN) < 3:
                await self.do(hatchery1.train(QUEEN))
            if self.can_afford(QUEEN) and hatchery2.noqueue and self.already_pending(QUEEN) < 3:
                await self.do(hatchery2.train(QUEEN))
                self.naturalBaseTag = 1
        
        if unit.type_id == HATCHERY:
        # When a new base is created we calculate the theoretical maximum number of workers we want to have in each of the bases
            if self.mainBaseTag != 0 and self.naturalBaseTag != 1:
                self.naturalBaseTag = unit.tag
            if self.can_afford(QUEEN):
                actions.append(unit.train(QUEEN))
            totalBaseCount = self.units(HATCHERY).amount + self.units(LAIR).amount + self.units(HIVE).amount
            if totalBaseCount < 4:
                self.workerCap =  totalBaseCount * 21
            else:
                self.workerCap = 66
        
        # The following two if statements just check if one can start upgrading the upgrades these
        # buildings offer immediately once they complete
        if unit.type_id == EVOLUTIONCHAMBER:
            evochamber = self.units(EVOLUTIONCHAMBER).ready
            if self.can_afford(RESEARCH_ZERGMELEEWEAPONSLEVEL1):
                actions.append(evochamber.first(RESEARCH_ZERGMELEEWEAPONSLEVEL1))
                self.groundUpgradeStarted = True

        if unit.type_id == SPIRE:
            spire = self.units(SPIRE).ready
            if self.can_afford(RESEARCH_ZERGFLYERATTACKLEVEL1):
                actions.append(spire.first(RESEARCH_ZERGFLYERATTACKLEVEL1))
                self.airUpgradeStarted = True
        
        await self.do_actions(actions)

    # The queue at this stage just allows for a more object oriented way of producing units. Where we don't
    # need to check if larvae exists for every different type of unit in unitProduction. Instead we simply put
    # the ID of the unit into the queue and take it out here and then produce it. 

    # This is more effective for units that have to created continously rather than units that have to created 
    # immediately.

    async def produceUnitsFromQueue(self, larvae, actions, unitQueue: PriorityQueue):
        for unit in unitQueue:
            if larvae.exists and self.can_afford(unit):
                actions.append(larvae.random.train(unitQueue.dequeue()))
            else:
                break

        await self.do_actions(actions)