from strategy_profile import StrategyProfile
from copy import deepcopy
from typing import Dict, List, Set
from player import Player
from resource import Resource

class Equilibrium():

    def __init__(self, players: Dict[int, Player], resources: Dict[int, Resource]):
        self.k = len(players)
        self.xD = dict() # key; int, value; int
        self.xA = dict() # key; int, value; int
        self.x = dict() # key; int, value; int

        self.players = players # key: int, value: Player
        self.resources = resources
        self.profile = self.step0()

    def tmp(self):
        return StrategyProfile({1: {1}, 2: {1}}, self.players, self.resources)

    def calculate_marginal_benefit(self, player, congestion, number_of_resources):
        return player.benefit * (self.resources[1].get_failure_probability(congestion)**(number_of_resources))

    def calculate_marginal_cost(self, congestion):
        return self.resources[1].get_cost(congestion)/(1-self.resources[1].get_failure_probability(congestion))

    def sigma(self, start, end, collection: dict):
        sum = 0
        for i in range(start, end + 1):
            if type(collection[i]) == set:
                sum += len(collection[i])
            elif type(collection[i]) == int:
                sum += collection[i]
        return sum

    def step0(self): # done
        player = min(self.players.values(), key=lambda x:x.benefit)
        if self.calculate_marginal_benefit(player, len(self.players), len(self.resources)-1) >= self.calculate_marginal_cost(len(self.players)): # player with the lowest benefit
            return StrategyProfile({key:set(self.resources.keys()) for key in self.players.keys()}, self.players, self.resources)
        else:
            self.k -= 1
            return self.step1()

    def step1(self): # done
        for player in self.players.values():
            XD = []
            for x in range(1, len(self.resources)+1):
                if self.calculate_marginal_benefit(player, self.k, x-1) >= self.calculate_marginal_cost(self.k):
                    XD.append(x)
            if XD == []:
                self.xD[player.id] = 0
            else:
                self.xD[player.id] = max(XD)
        if sum(self.xD.values()) < self.k * len(self.resources):
            self.k -= 1
            return self.step2()
        else:
            return self.step3()

    def step2(self): # done
        if self.k == 0:
            strategies = dict()
            resource_index = 1
            for player in self.players.values():
                if self.xD[player.id] > 0:
                    strategy = set()
                    for i in range(resource_index, resource_index + self.xD[player.id]): # change to while to ensure player get enough resources
                        strategy.add(self.resources[i].id)
                    resource_index += self.xD[player.id]
                    strategies[player.id] = strategy
                else:
                    strategies[player.id] = set()
            return StrategyProfile(strategies, self.players, self.resources)
        else:
            return self.step1()

    def step3(self):
        for player in self.players.values():
            XA = []
            for x in range(len(self.resources)):
                if self.calculate_marginal_benefit(player, self.k, x) <= self.calculate_marginal_cost(self.k+1):
                    XA.append(x)
            if XA == []:
                self.xA[player.id] = len(self.resources)
            else:
                self.xA[player.id] = min(XA)
        if sum(self.xA.values()) > self.k * len(self.resources) or any(self.xA[player_id] > self.xD[player_id] for player_id in self.players.keys()):
            return self.step5() # k*-even, post-addition D-stable profile
        else:
            return self.step4()

    def step4(self): # profile is k*-even, D-stable
        d = dict()
        strategies = {key:set() for key in self.players.keys()}
        resource_index = 1
        ##print(f'Init. resource_index: {resource_index}')
        for i in range(1, len(self.players) + 1):
            d[i] = self.k * len(self.resources) - self.sigma(1, i - 1, strategies) - self.sigma(i, len(self.players), self.xA)
            r = min([self.xD[i], self.xA[i] + d[i]]) # the number of resources player will receive
            if resource_index == len(self.resources):
                resource_index = 1
            strategy = set()

            while r > 0:
                if resource_index == 0:
                    resource_index = len(self.resources)
                strategy.add(resource_index)
                resource_index = (resource_index + 1) % len(self.resources)
                r -= 1
            strategies[self.players[i].id] = strategy # needs to be fixed to link strategy and player
        #self.profile = StrategyProfile(strategies, self.players, self.resources)
        return StrategyProfile(strategies, self.players, self.resources)

    def step5(self): # needs research in the same way as step4, profile is k*-even D-stable not A-stable
        for player in self.players.values():
            X = []
            for x in range(1, len(self.resources)):
                if self.calculate_marginal_benefit(player, self.k, x - 1) >= self.calculate_marginal_cost(self.k + 1): # check this line
                    X.append(x)
            if X == []:
                self.x[player.id] = 0
            else:
                self.x[player.id] = max(X)
        resource_index = 1
        strategies = {key:set() for key in self.players.keys()}
        for i in range(1, len(self.players) + 1):
            delta = self.k * len(self.resources) - self.sigma(1, i - 1, strategies)
            if delta > 0:
                r = min([self.x[i], delta])
                strategy = set()
                if resource_index == 0:
                    resource_index = len(self.resources)
                while r > 0:
                    if resource_index == 0:
                        resource_index = len(self.resources)
                    strategy.add(resource_index)
                    resource_index = (resource_index + 1) % len(self.resources)
                    r -= 1
                strategies[i] = strategy
            else:
                strategies[i] = set()
        return self.step6(StrategyProfile(strategies, self.players, self.resources))

    def step6(self, strategy_profile): # done
        a_move_resources = dict() # M(sigma)
        for player in self.players.values():
            option = {key:value for key, value in strategy_profile.congestion.items() if not key in strategy_profile.strategies[player.id]}
            light_resource = None
            if len(option) > 0:
                light_resource = min(option, key=option.get)
            new_strategy = deepcopy(strategy_profile.strategies[player.id])
            new_strategy.add(light_resource)
            if light_resource != None and strategy_profile.simulate_change(new_strategy, player.id):
                a_move_resources[player.id] = light_resource
        if len(a_move_resources) == 0:
            return strategy_profile
        else:
            return self.step7(strategy_profile, a_move_resources)

    def step7(self, strategy_profile, a_move_resources):
        a_move_player, light_resource_a = min(a_move_resources.items(), key=lambda x: x[1])
        
        if light_resource_a == min(strategy_profile.congestion.items(), key=lambda x: x[1])[0]:
            strategy_profile.strategies[a_move_player].update({light_resource_a})
        else:
            light_resource_b = min(strategy_profile.congestion, key=strategy_profile.congestion.get)
            player_j = [key for key, value in strategy_profile.strategies.items() if light_resource_a in value and not light_resource_b in value][0]
            strategy_profile.strategies[a_move_player].update({light_resource_a})
            strategy_profile.strategies[player_j].update({light_resource_b})
        strategy_profile.update_profile()
        return self.step6(strategy_profile)