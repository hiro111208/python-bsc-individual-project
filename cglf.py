import itertools
import copy
import strategy_profile as sp
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
            self.strategy_profiles.append(sp.StrategyProfile(strategy_profile, self.players, self.resources))

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

        """ for player in self.players:
            for k_even_profile in even_profiles[k]:
                for even_profile in even_profiles[k-1]:
                    if k_even_profile.utilities >= even_profile[player]
        for player in self.players:
            v = player.benefit * (failure_probability(n) ** (m-1))
            x = 
            vikx = player.benefit * (failure_probability(k) ** x)
        if v > c:
            return "strategy profile in which all players choose all resources"
        else:
            k -= 1
            # go to step1 """

    """ def step1(self):
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
            strategy_profiles = self.strategy_profiles
            for player in self.players:
                if xD[player] > 0:
                    strategy_profiles = list(filter(lambda x: len(x.strategies[player]) == xD[player]))
                else:
                    strategy_profiles = list(filter(lambda x: x.strategies[player] == set()))
            return strategy_profiles[0]
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
            print(f'Go to step5') """

    """ def step4(self):
        for player in self.players:

    def step5(self):
        for player in self.players:
            set resources
        if resources != []:
            return
        else:

    def step6(self):
        for player in self.players:
            select minimum resource
        set strategy_profile = 
        if strategy_profile == []:
            return

    def step7(self):
        set M
        select min congestion a and player i
        if a is min:
            i's strategy = strategy + a
        else:
            select min congestion b and player j
            i's strategy = strategy + a
            j's strategy = strategy - a + b
            go to step6 """