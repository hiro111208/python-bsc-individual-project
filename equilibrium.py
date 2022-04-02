from strategy_profile import StrategyProfile
from copy import deepcopy
from typing import Dict, List, Set
from player import Player
from resource import Resource

class Equilibrium():

    def __init__(self, players: Dict[int, Player], resources: Dict[int, Resource]):
        self.__k = len(players)
        self.__xD = dict() # key; int, value; int
        self.__xA = dict() # key; int, value; int
        self.__x = dict() # key; int, value; int

        self.__players = players # key: int, value: Player
        self.__resources = resources
        self.__profile = self.step0()

    def tmp(self):
        return StrategyProfile({1: {1}, 2: {1}}, self.__players, self.__resources)

    def calculate_marginal_benefit(self, player, congestion, number_of_resources):
        return player.get_benefit() * (self.__resources[1].get_failure_probability(congestion)**(number_of_resources))

    def calculate_marginal_cost(self, congestion):
        return self.__resources[1].get_cost(congestion)/(1-self.__resources[1].get_failure_probability(congestion))

    def sigma(self, start, end, collection: dict):
        sum = 0
        for i in range(start, end + 1):
            if type(collection[i]) == set:
                sum += len(collection[i])
            elif type(collection[i]) == int:
                sum += collection[i]
        return sum

    def get_equilibrium_profile(self) -> StrategyProfile:
        return self.__profile

    def step0(self): # done
        player = min(self.__players.values(), key=lambda x:x.get_benefit())
        if self.calculate_marginal_benefit(player, len(self.__players), len(self.__resources)-1) >= self.calculate_marginal_cost(len(self.__players)): # player with the lowest benefit
            return StrategyProfile({key:set(self.__resources.keys()) for key in self.__players.keys()}, self.__players, self.__resources)
        else:
            self.__k -= 1
            return self.step1()

    def step1(self): # done
        for player in self.__players.values():
            XD = []
            for x in range(1, len(self.__resources)+1):
                if self.calculate_marginal_benefit(player, self.__k, x-1) >= self.calculate_marginal_cost(self.__k):
                    XD.append(x)
            if XD == []:
                self.__xD[player.get_id()] = 0
            else:
                self.__xD[player.get_id()] = max(XD)
        if sum(self.__xD.values()) < self.__k * len(self.__resources):
            self.__k -= 1
            return self.step2()
        else:
            return self.step3()

    def step2(self): # done
        if self.__k == 0:
            strategies = dict()
            resource_index = 1
            for player in self.__players.values():
                if self.__xD[player.get_id()] > 0:
                    strategy = set()
                    for i in range(resource_index, resource_index + self.__xD[player.get_id()]): # change to while to ensure player get enough resources
                        strategy.add(self.__resources[i].get_id())
                    resource_index += self.__xD[player.get_id()]
                    strategies[player.get_id()] = strategy
                else:
                    strategies[player.get_id()] = set()
            return StrategyProfile(strategies, self.__players, self.__resources)
        else:
            return self.step1()

    def step3(self):
        for player in self.__players.values():
            XA = []
            for x in range(len(self.__resources)):
                if self.calculate_marginal_benefit(player, self.__k, x) <= self.calculate_marginal_cost(self.__k+1):
                    XA.append(x)
            if XA == []:
                self.__xA[player.get_id()] = len(self.__resources)
            else:
                self.__xA[player.get_id()] = min(XA)
        if sum(self.__xA.values()) > self.__k * len(self.__resources) or any(self.__xA[player_id] > self.__xD[player_id] for player_id in self.__players.keys()):
            return self.step5() # k*-even, post-addition D-stable profile
        else:
            return self.step4()

    def step4(self): # profile is k*-even, D-stable
        d = dict()
        strategies = {key:set() for key in self.__players.keys()}
        resource_index = 1
        ##print(f'Init. resource_index: {resource_index}')
        for i in range(1, len(self.__players) + 1):
            d[i] = self.__k * len(self.__resources) - self.sigma(1, i - 1, strategies) - self.sigma(i, len(self.__players), self.__xA)
            r = min([self.__xD[i], self.__xA[i] + d[i]]) # the number of resources player will receive
            if resource_index == len(self.__resources):
                resource_index = 1
            strategy = set()

            while r > 0:
                if resource_index == 0:
                    resource_index = len(self.__resources)
                strategy.add(resource_index)
                resource_index = (resource_index + 1) % len(self.__resources)
                r -= 1
            strategies[self.__players[i].get_id()] = strategy # needs to be fixed to link strategy and player
        #self.__profile = StrategyProfile(strategies, self.__players, self.__resources)
        return StrategyProfile(strategies, self.__players, self.__resources)

    def step5(self): # needs research in the same way as step4, profile is k*-even D-stable not A-stable
        for player in self.__players.values():
            X = []
            for x in range(1, len(self.__resources)):
                if self.calculate_marginal_benefit(player, self.__k, x - 1) >= self.calculate_marginal_cost(self.__k + 1): # check this line
                    X.append(x)
            if X == []:
                self.__x[player.get_id()] = 0
            else:
                self.__x[player.get_id()] = max(X)
        resource_index = 1
        strategies = {key:set() for key in self.__players.keys()}
        for i in range(1, len(self.__players) + 1):
            delta = self.__k * len(self.__resources) - self.sigma(1, i - 1, strategies)
            if delta > 0:
                r = min([self.__x[i], delta])
                strategy = set()
                if resource_index == 0:
                    resource_index = len(self.__resources)
                while r > 0:
                    if resource_index == 0:
                        resource_index = len(self.__resources)
                    strategy.add(resource_index)
                    resource_index = (resource_index + 1) % len(self.__resources)
                    r -= 1
                strategies[i] = strategy
            else:
                strategies[i] = set()
        return self.step6(StrategyProfile(strategies, self.__players, self.__resources))

    def step6(self, strategy_profile): # done
        a_move_resources = dict() # M(sigma)
        for player in self.__players.values():
            strategies = strategy_profile.get_strategies()
            option = {key:value for key, value in strategy_profile.get_congestion().items() if not key in strategies[player.get_id()]}
            light_resource = None
            if len(option) > 0:
                light_resource = min(option, key=option.get)
            new_strategy = deepcopy(strategies[player.get_id()])
            new_strategy.add(light_resource)
            if light_resource != None and strategy_profile.simulate_change(new_strategy, player.get_id()):
                a_move_resources[player.get_id()] = light_resource
        if len(a_move_resources) == 0:
            return strategy_profile
        else:
            return self.step7(strategy_profile, a_move_resources)

    def step7(self, strategy_profile, a_move_resources):
        a_move_player, light_resource_a = min(a_move_resources.items(), key=lambda x: x[1])
        strategies = strategy_profile.get_strategies()
        
        if light_resource_a == min(strategy_profile.get_congestion().items(), key=lambda x: x[1])[0]:
            strategies[a_move_player].update({light_resource_a})
        else:
            light_resource_b = min(strategy_profile.get_congestion(), key=strategy_profile.get_congestion().get)
            player_j = [key for key, value in strategies.items() if light_resource_a in value and not light_resource_b in value][0]
            strategies[a_move_player].update({light_resource_a})
            strategies[player_j].update({light_resource_b})
        strategy_profile.update_profile()
        return self.step6(strategy_profile)