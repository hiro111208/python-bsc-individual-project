import itertools
import copy


class CGLF():

    # utility = strategy_profiles[player][all player's strategy]

    def __init__(self, players, resources):
        self.players = players
        self.resources = resources
        self.strategy_profiles = list()
        self.set_strategy_profiles()
        self.utilities = None

    def set_strategy_profiles(self):
        #dictionary of key (player, strategy)
        # carteisan product
        strategy_sets = []
        for player in self.players:
            player.set_strategy_set(self.resources)
            strategy_sets.append(player.get_strategy_set())
        strategy_combinations = list(itertools.product(*strategy_sets))
        for strategy_combination in strategy_combinations:
            congestion = self.get_congestion(strategy_combination)
            utilities = dict()
            for item in strategy_combination:
                player = item[0]
                strategy = item[1]
                utility = self.calculate_utility(player, strategy, congestion)
                utilities[player] = utility
            self.strategy_profiles.append((strategy_combination, utilities))
        #self.strategy_profiles = list(itertools.product(*strategy_sets))


    def get_strategy_profiles(self):
        try:
            return self.strategy_profiles
        except:
            print("Strategy profiles have not been defined.")

    def get_congestion(self, strategy_profile):
        congestion = {key: 0 for key in self.resources}
        for element in strategy_profile:
            for resource in element[1]:
                congestion[resource] += 1
        return congestion
    
    def get_utility(self):
        choices = {key: None for key in self.players}
        print(f'Choose Player from below')
        for i in range(len(self.players)):
            print(f'{i}: Player {self.players[i].get_id()}')
        index = input('Enter number: ')
        target_player = self.players[int(index)]
        strategy_profiles = copy.deepcopy(self.strategy_profiles)
        for player in self.players:
            print(f'Choose a strategy of Player {target_player.get_id()} from below')
            strategy_set = player.get_strategy_set()
            for i in range(len(strategy_set)):
                resource_id = ""
                if player.get_strategy_set()[i][1] == []:
                    resource_id = "Empty"
                else:
                    for resource in player.get_strategy_set()[i][1]:
                        resource_id += (resource.get_id() + " ")
                #print(resource_id)
                print(f'{i}: {resource_id}')
            number = input('Enter number: ') # must be below the length of resources
            index = int(number)
            #print(len(strategy_profiles))
            #strategy_profiles = list(filter(lambda strategy_profile: (strategy_set[index]) in list(strategy_profile[0]), strategy_profiles))
            #print(len(strategy_profiles))
            choices[player] = strategy_set[index]
        strategy_profile_key = []
        for player in self.players:
            strategy_profile_key.append((choices[player]))
        for strategy_profile in self.strategy_profiles:
            if strategy_profile_key == list(strategy_profile[0]):
                return strategy_profile[1][target_player]

    
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
        # step 6
        for player in self.players:
            resources = copy.deepcopy(self.resources)
            for resource in player.strategy:
                if resource in resources:
                    resources.remove(resource)
            profitable_resources = []
            for resource in resources:
                player
            e_i # e_i: such that unilaterally additing this is profitable """