import itertools
import copy
from strategy_profile import StrategyProfile
import collections


class CGLF():

    def __init__(self, players, resources):
        self.players = players
        """ self.players = dict()
        for i in range(len(players)):
            self.players[i] = players[i] """
        self.resources = resources
        """ self.resources = dict()
        for i in range(len(resources)):
            self.resources[i] = resources[i] """
        self.number_of_profiles = 0
        
        self.strategy_set = self.set_strategy_set(resources)
        self.strategy_profiles = list()

        self.build_strategy_profiles()

    
    def set_strategy_set(self, resources): # strategies that player can choose
        strategy_set = []
        for i in range(len(resources)+1):
            for strategy in itertools.combinations(resources, i):
                strategy_set.append(set(list(strategy)))
        return strategy_set

    def build_strategy_profiles(self):
        strategy_sets = dict()
        for player in self.players:
            strategy_sets[player] = self.strategy_set
        product = [x for x in itertools.product(*strategy_sets.values())]
        strategy_profiles = [dict(zip(strategy_sets.keys(), r)) for r in product]
        for strategy_profile in strategy_profiles:
            self.strategy_profiles.append(StrategyProfile(strategy_profile, self.players, self.resources))

    """ def build_strategy_profiles(self):
        strategy_sets = dict()
        for player in self.players:
            # player.set_strategy_set(self.resources)
            # strategy_sets[player] = player.get_strategy_set()
            strategy_sets[player] = self.strategy_set
        strategy_profiles = itertools.product(strategy_sets, len(self.players))
        for strategy_profile in strategy_profiles:
            self.strategy_profiles.append(sp.StrategyProfile(strategy_profile, self.players, self.resources)) """

    def get_utility(self):
        choices = {key: None for key in self.players} # dict key: player, value: player's strategy
        print(f'Choose Player from below')
        players = list(self.players)
        for i in range(len(players)):
            print(f'{i}: Player {players[i].get_id()}')
        index = input('Enter number: ')
        target_player = players[int(index)]
        print(f'Target player chosen: {target_player.get_id()}')
        for player in players:
            print(f'{player.get_id()} is in a set: {player in self.players}')
            print(f'Choose a strategy of Player {player.get_id()} from below')
            for i in range(len(self.strategy_set)):
                resource_name = ""
                if self.strategy_set[i] == set():
                    resource_name = "Empty"
                else:
                    for resource in self.strategy_set[i]:
                        resource_name += (str(resource.get_name()) + " ")
                print(f'{i}: {resource_name}')
            number = input('Enter number: ') # must be below the length of resources
            index = int(number)
            #print(len(self.strategy_profiles))
            choices[player] = self.strategy_set[index]
        # print(f'choices: {choices}')
        for strategy_profile in self.strategy_profiles:
            equality = []
            for player in strategy_profile.strategies.keys(): # strategy is supposed to be set
                equality.append(strategy_profile.strategies[player]==choices[player])
            # print(f'equality: {equality}')
            if set(equality) == {True}:
                print(f'even: {strategy_profile.even}')
                return strategy_profile.utilities[target_player]

    """ def find_nash_equilibrium(self):
        # step 1 - determine k*
        # step 6
        for player in self.players:
            resources = copy.deepcopy(self.resources)
            for resource in player.strategy:
                if resource in resources:
                    resources.remove(resource)
            profitable_resources = []
            for resource in resources:
                player
            e_i # e_i: such that unilaterally additing this is profitable

    def find_d_stable_strategy_profiles(self, strategy_profiles): # there's no player with profitable d-move from the strategy profile
        k = len(self.players)
        m = len(self.resources)
        for d_strategy_profile in reversed(strategy_profiles):
            for strategy_profile in strategy_profiles:
                for player in self.players:
                    if len(d_strategy_profile['strategy_profile'][player]) > len(strategy_profile['strategy_profile'][player]):
                        if d_strategy_profile['utilities'][player] <  strategy_profile['utilities'][player]: # utility
                            strategy_profiles.remove(d_strategy_profile)
                            print(f'To be removed: {d_strategy_profile}')
                            break
                else:
                    continue
                break
        return strategy_profiles """

    def calculate_marginal_benefit(self, player, congestion, number_of_resources):
        return player.benefit * (self.resources[0].get_failure_probability(congestion)**(number_of_resources))

    def calculate_marginal_cost(self, congestion):
        return self.resources[0].get_cost(congestion)/(1-self.resources[0].get_failure_probability(congestion))
        
    def step0(self):
        print(f'Step0 called')
        k = len(self.players)
        even_profiles = collections.defaultdict(list)
        for strategy_profile in self.strategy_profiles:
            if strategy_profile.even != None:
                even_profiles[strategy_profile.even].append(strategy_profile)

        for player in self.players:
            for k_even_profile in even_profiles[k]:
                #marginal_benefit = player.benefit * (self.resources[0].get_failure_probability(len(self.players))**(len(self.resources)-1))
                marginal_benefit = self.calculate_marginal_benefit(player, k, len(self.resources)-1)
                #marginal_cost = self.resources[0].get_cost(len(self.players))/(1-self.resources[0].get_failure_probability(len(self.players)))
                marginal_cost = self.calculate_marginal_cost(k)
                if marginal_benefit < marginal_cost:
                    k -= 1
                    print(f'Go to step1')
                    return even_profiles[k][0]
        print(f'Found equilibrium')
        return even_profiles[k][0]

    def step1(self):
        k = len(self.players)-1
        xD = dict()
        for player in self.players:
            XD = []
            for x in range(1, len(self.resources)+1):
                if self.calculate_marginal_benefit(player, k, x-1) >= self.calculate_marginal_cost(k):
                    XD.append(x)
            if XD == []:
                xD[player] = 0
            else:
                xD.append(max(X))
                xD[player] = max(X)
        if sum(xD.values()) < k * len(self.resources):
            k -= 1
            print(f'Go to step2')
        else:
            print(f'Go to step3')

    def step2(self, strategy_profiles):
        if k = 0:
            #strategy_profiles = self.strategy_profiles
            strategies = dict()
            resource_index = 1
            for player in self.players:
                if xD[player] > 0:
                    strategy = set()
                    for i in range(resource_index, xD[player] + 1):
                        strategy.add(self.resources[i])
                    resource_index += xD[player]
                    strategies[player] = strategy
                    #strategy_profiles = list(filter(lambda x: len(x.strategies[player]) == xD[player]))
                else:
                    strategies[player] = set()
                    #strategy_profiles = list(filter(lambda x: x.strategies[player] == set()))
            #return strategy_profiles[0]
            return StrategyProfile(strategies, self.players, self.resources)
        else:
            print(f'Go to step1')

    def step3(self, strategy_profiles):
        k = len(self.players)-1
        xA = dict()
        for player in self.players:
            XA = []
            for x in range(len(self.resources)):
                if self.calculate_marginal_benefit(player, k, x) >= self.calculate_marginal_cost(k+1):
                    XA.append(x)
            if XA == []:
                xA[player] = len(self.resources)
            else:
                xA[min] = min(X)
        if sum(xA.values()) > k * len(self.resources) or any(xa[key] > xd[key] for key in xA.keys()):
            print(f'Go to step5')

    def step4(self):
        strategies = dict()
        for player in self.players:
            di = k*m - self.sigma(1, i, len(sp.strategies[j])) - self.sigma(i, len(self.players), xA[j])
            r = min([xD, xA + di])
            strategy = set()
            for i in range(resource_index, r + 1):
                strategy.add(self.resources[i])
            resource_index = (resource_index + r) % len(self.resources)
            strategies[player] = strategy
        return StrategyProfile(strategies, self.players, self.resources)


    def step5(self):
        X = []
        for player in self.players:
            Xi = []
            for x in range(1, len(self.resources) + 1):
                if self.calculate_marginal_benefit(player, k, x-1) <= self.calculate_marginal_cost(k + 1):
                    Xi.append(x)
            X.append(Xi)
        x = []
        for Xi in X:
            if Xi == []:
                x.append(0)
            else:
                x.append(max(Xi))
        resource_index = 1
        for i in range(self.players):
            r = min(x[i], km - self.sigma(1, i, len(sp.strategies[j])))
            if km - self.sigma(1, i, len(sp.strategies[j])) > 0:
                strategy = set()
                for i in range(resource_index, r + 1):
                    strategy.add(self.resources[i])
                strategies[player] = strategy
                resource_index = (resource_index + r) % len(self.resources)
            else:
                strategy[player] = set()

        for player in self.players:
            set resources
        if resources != []:
            return
        else:

    def step6(self, strategy_profile):
        for player in self.players:
            option = {x: strategy_profile.get_congestion()[x] for x in strategy_profile.get_congestion() if x not in strategies[player]}
            light_resource = min(option, key=option.get)
        a_move_players = []
        for player in self.players:
            if new_sp > current_sp:
                a_move_players.append(player)
        if len(a_move_players) == 0:
            return strategy_profile

    def step7(self, strategy_profile):
        a_move_resources = [] # M(sigma)
        for resource in self.resources:
            for player in self.players:
                if new_sp > current_sp: # new_sp means strategy with a resouce which player finds beneficial to add
                    a_move_resources.append(resource)
        light_resource = min_congestion(a_move_resources)
        a_move_player = a_move_players_from_step6[player who wanna use light resource]
        if light_resource min_congestion(strategy_profile):
            # one step addition
            strategies[a_move_player] = strategies[a_move_player].update({light_resource})
            # back to step6
        else:
            # two step addition
        select min congestion a and player i
        if a is min:
            i's strategy = strategy + a
        else:
            select min congestion b and player j
            i's strategy = strategy + a
            j's strategy = strategy - a + b
            go to step6

    def sigma(start, end, collection) -> float:
        sum = 0
        for i in range(start, end + 1):
            sum += collection[i]
        return sum

    def calculate_marginal_benefit(self, player, congestion, number_of_resources):
        return player.benefit * (self.resources[0].get_failure_probability(congestion)**(number_of_resources))

    def calculate_marginal_cost(self, congestion):
        return self.resources[0].get_cost(congestion)/(1-self.resources[0].get_failure_probability(congestion))

    def equilibrium_finder(self):
        print(f'step0')
        k = len(self.players)
        """ even_profiles = collections.defaultdict(list)
        for strategy_profile in self.strategy_profiles:
            if strategy_profile.even != None:
                even_profiles[strategy_profile.even].append(strategy_profile)

        for player in self.players:
            for k_even_profile in even_profiles[k]: """
        player = min(self.players, key=lambda x::x.benefit)
        if self.calculate_marginal_benefit(player, k, len(self.resources)-1) >= self.calculate_marginal_cost(k): # player with the lowest benefit
            print(f'Found equilibrium')
            return even_profiles[k][0]
        else:
            k -= 1
            print(f'step1')
            xD = dict()
            for player in self.players:
                XD = []
                for x in range(1, len(self.resources)+1):
                    if self.calculate_marginal_benefit(player, k, x-1) >= self.calculate_marginal_cost(k):
                        XD.append(x)
                if XD == []:
                    xD[player] = 0
                else:
                    # xD.append(max(X))
                    xD[player] = max(X)
            if sum(xD.values()) < k * len(self.resources):
                k -= 1
                print(f'step2')
            else:
                print(f'step3')
                xA = dict()
                for player in self.players:
                    XA = []
                    for x in range(len(self.resources)):
                        if self.calculate_marginal_benefit(player, k, x) >= self.calculate_marginal_cost(k+1):
                            XA.append(x)
                    if XA == []:
                        xA[player] = len(self.resources)
                    else:
                        xA[player] = min(XA)
                if sum(xA.values()) > k * len(self.resources) or any(xa[player] > xd[player] for player in self.players):
                    print(f'step5') # k*-even, post-addition D-stable profile
                    x = dict()
                    for player in self.players:
                        X = []
                        for x in range(1, len(self.resources) + 1):
                            if self.calculate_marginal_benefit(player, k, x-1) <= self.calculate_marginal_cost(k + 1):
                                X.append(x)
                        if X == []:
                            x[player] = 0
                        else:
                            x[player] = max(X)
                    resource_index = 1
                    strategies = dict()
                    for i in range(1, self.players + 1):
                        strategy_sum = 0
                        for j in range(1, i):
                            strategy_sum += len(sp.strategies[j]) # Specify sp
                        comparison = k * len(self.resources) - strategy_sum
                        if comparison > 0: # 
                            strategy = set()
                            r = min([x[i], comparison])
                            for num in range(resource_index, r + 1):
                                strategy.add(self.resources[num])
                            strategies[player] = strategy
                            resource_index = (resource_index + r) % len(self.resources)
                        else:
                            strategy[player] = set()
                    print(f'step6') # confused
                    a_move_players = []
                    a_move_resources = [] # M(sigma)
                    # sp ; strategy profile
                    for player in self.players:
                        # option = {x: strategy_profile.get_congestion()[x] for x in strategy_profile.get_congestion() if x not in strategies[player]}
                        option = self.resources.difference_update(strategies[player])
                        light_resource = min(option, key=option.get)
                        if sp.simulate_change(sp.strategies[player].add(light_resource), player):
                            a_move_players.append(player)
                            a_move_resources.append(light_resource)
                            # a_move_resources[player] = light_resource
                    if len(a_move_players) == 0:
                        return sp
                    print(f'step7')
                    sp = social optimum profile
                    # a_move_resources = [] # M(sigma)
                    light_resource = min_congestion(a_move_resources)
                    a_move_player = a_move_players_from_step6[player who wanna use light resource]
                    # a_move_player, light_resource_a = min(a_move_resources.items(), key=lambda x: x[1])
                    if light_resource min_congestion(sp):
                        # one step addition
                        strategies[a_move_player] = strategies[a_move_player].update({light_resource})
                        # back to step6
                    else:
                        # two step addition
                        light_resource_b = min congestion(sp)
                        player_j = player using light_resource_a
                        strategies[a_move_player] = strategies[a_move_player].update({light_resource})
                        strategies[player_j] = strategies[player_j].difference_update(light_resource_a)
                        strategies[player_j] = strategies[player_j].update(light_resource_b)
                    print(f'back to step6')