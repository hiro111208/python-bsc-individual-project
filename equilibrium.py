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
        # self.step0()
        # self.step6(profile)

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
            else:
                sum += collection[i]
        return sum

    def step0(self): # done
        player = min(self.players.values(), key=lambda x:x.benefit)
        if self.calculate_marginal_benefit(player, len(self.players), len(self.resources)-1) >= self.calculate_marginal_cost(len(self.players)): # player with the lowest benefit
            #print(f'Found equilibrium')
            #self.profile = StrategyProfile({key:self.resources.keys() for key in self.players.keys()}, self.players, self.resources)
            return StrategyProfile({key:self.resources.keys() for key in self.players.keys()}, self.players, self.resources)
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
                # self.xD.append(max(X))
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
            #self.profile = StrategyProfile(strategies, self.players, self.resources)
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
            for x in range(1, len(self.resources) + 1):
                if self.calculate_marginal_benefit(player, self.k, x - 1) <= self.calculate_marginal_cost(self.k + 1):
                    X.append(x)
            if X == []:
                self.x[player.id] = 0
            else:
                self.x[player.id] = max(X)
        resource_index = 1
        strategies = {key:set() for key in self.players.keys()}
        for i in range(1, len(self.players) + 1):

            if self.k * len(self.resources) - self.sigma(1, i - 1, strategies) > 0:
                r = min([self.x[i], self.k * len(self.resources) - self.sigma(1, i - 1, strategies)])
                strategy = set()
                if resource_index == 0:
                    resource_index = len(self.resources)
                while r > 0:
                    if resource_index == 0:
                        resource_index = len(self.resources)
                    strategy.add(resource_index)
                    resource_index = (resource_index + 1) % len(self.resources)
                    r -= 1
                strategies[player.id] = strategy # needs to be fixed to link strategy and player
            else:
                strategies[player.id] = set() # needs to be fixed to link strategy and player
        return self.step6(StrategyProfile(strategies, self.players, self.resources))

    def step6(self, strategy_profile): # done
        # a_move_players = []
        a_move_resources = dict() # M(sigma)
        for player in self.players.values():
            # option = {x: strategy_profile.get_congestion()[x] for x in strategy_profile.get_congestion() if x not in strategies[player]}
            option = {key:value for key, value in strategy_profile.congestion.items() if not key in strategy_profile.strategies[player.id]}
            light_resource = None
            if len(option) > 0:
                light_resource = min(option, key=option.get) # option must be dict
            new_strategy = deepcopy(strategy_profile.strategies[player.id])
            new_strategy.add(light_resource)
            if light_resource != None and strategy_profile.simulate_change(new_strategy, player.id):
                #a_move_players.append(player)
                #a_move_resources.append(light_resource)
                a_move_resources[player.id] = light_resource
        if len(a_move_resources) == 0:
            # the profile is confirmed to be A-stable
            #self.profile = strategy_profile
            return strategy_profile
        else:
            return self.step7(strategy_profile, a_move_resources)

    def step7(self, strategy_profile, a_move_resources): # done
        a_move_player, light_resource_a = min(a_move_resources.items(), key=lambda x: x[1])
        #print(f'a_move_player: {a_move_player}')
        #print(f'light_resource_a: {light_resource_a}')
        
        if light_resource_a == min(strategy_profile.congestion.items(), key=lambda x: x[1])[0]:
            # one step addition
            # strategy_profile.strategies[a_move_player] = strategies[a_move_player].update({light_resource_a})
            strategy_profile.strategies[a_move_player].update({light_resource_a})
            #print(f'a* resource added')
        else:
            # two step addition
            #print(f'entered two-step addition')
            #print(f'trying')
            light_resource_b = min(strategy_profile.congestion, key=strategy_profile.congestion.get)
            """ if len([key for key, value in strategy_profile.strategies.items() if (light_resource_a in value)]) > 0:
                #print(f'a: {light_resource_a}')
                #print(f'b: {light_resource_b}')
                #print(f'players haveing resource a, not b')
            else:
                #print(f'it wasnt') """
        #try:
            player_j = [key for key, value in strategy_profile.strategies.items() if light_resource_a in value and not light_resource_b in value][0]
            """ if player_j == None:
                #print(f'player j not found') """
            strategy_profile.strategies[a_move_player].update({light_resource_a})
            strategy_profile.strategies[player_j].difference_update({light_resource_a})
            strategy_profile.strategies[player_j].update({light_resource_b})
            #print(f'a* and b* resource added')
        #except:
            #print(f'something went wrong')
            #print(f'light_resource_a; {light_resource_a}')
            #print(f'light_resource_b; {light_resource_b}')
            #print(str(([f'key: {key}, value: {strategy_profile.strategies[key]}' for key, value in strategy_profile.strategies.items() if light_resource_a in value])))
            
        strategy_profile.update_congestion()
        return self.step6(strategy_profile)