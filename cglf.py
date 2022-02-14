import itertools
import copy


class CGLF():

    # utility = strategy_profiles[player][all player's strategy]

    def __init__(self, players, resources):
        self.players = players
        self.resources = resources
        self.pay_off_matrix = list()
        self.set_pay_off_matrix()
        self.number_of_profiles = 0

    def set_pay_off_matrix(self):
        #dictionary of key (player, strategy)
        # carteisan product
        # strategy_sets = [] # strategy set of each player
        strategy_sets = dict()
        for player in self.players:
            player.set_strategy_set(self.resources)
            strategy_sets[player] = player.get_strategy_set()
        product = [x for x in itertools.product(*strategy_sets.values())]
        strategy_profiles = [dict(zip(strategy_sets.keys(), r)) for r in product]
        for strategy_profile in strategy_profiles:
            congestion = self.get_congestion(strategy_profile)
            utilities = dict()
            for player, strategy in strategy_profile.items():
                utility = self.calculate_utility(player, strategy, congestion)
                utilities[player] = utility
            self.pay_off_matrix.append({'strategy_profile':strategy_profile, 'utilities':utilities})
        self.number_of_profiles = len(self.pay_off_matrix)
        print(f'Number of profiles: {self.number_of_profiles}')


    def get_pay_off_matrix(self):
        try:
            return self.pay_off_matrix
            # list of tuples, each tuple contains a strategy profile (tuple) and utilities of each player (dict), 
            # each item in strategy profile contains a player and its strategy
        except:
            print("Strategy profiles have not been defined.")

    def get_congestion(self, strategy_profile): # strategy profile is dict of 
        congestion = {key: 0 for key in self.resources}
        for element in strategy_profile.values():
            for resource in element:
                congestion[resource] += 1
        return congestion
    
    def get_utility(self):
        choices = {key: None for key in self.players} # dict key: player, value: player's strategy
        print(f'Choose Player from below')
        for i in range(len(self.players)):
            print(f'{i}: Player {self.players[i].get_id()}')
        index = input('Enter number: ')
        target_player = self.players[int(index)]
        strategy_profiles = copy.deepcopy(self.pay_off_matrix)
        for player in self.players:
            print(f'Choose a strategy of Player {target_player.get_id()} from below')
            strategy_set = player.get_strategy_set()
            for i in range(len(strategy_set)):
                resource_id = ""
                if player.get_strategy_set()[i] == []:
                    resource_id = "Empty"
                else:
                    for resource in player.get_strategy_set()[i]:
                        resource_id += (resource.get_id() + " ")
                print(f'{i}: {resource_id}')
            number = input('Enter number: ') # must be below the length of resources
            index = int(number)
            #print(len(strategy_profiles))
            #strategy_profiles = list(filter(lambda strategy_profile: (strategy_set[index]) in list(strategy_profile[0]), strategy_profiles))
            #print(len(strategy_profiles))
            choices[player] = strategy_set[index]
        for cell in self.pay_off_matrix:
            if choices == cell['strategy_profile']:
                return cell['utilities'][target_player]

    def calculate_utility(self, player, strategy, congestion):
        # strategy is a list of resources
        probability_product = 1
        total_cost = 0
        for resource in strategy:
            failure_probability = resource.get_failure_probability(congestion[resource]-1)
            cost = resource.get_cost(congestion[resource]-1)
            probability_product *= failure_probability
            total_cost += cost
        utility = player.get_benefit()*(1-probability_product) - total_cost
        return utility

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
        for strategy_profile in strategy_profiles:

        return profiles """