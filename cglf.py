import itertools


class CGLF():

    def __init__(self, players, resources):
        self.players = players
        self.resources = resources
        self.strategy_profiles = None
        self.set_strategy_profiles()
        self.utilities = None

    def set_strategy_profiles(self):
        #dictionary of key (player, strategy)
        # carteisan product
        strategy_sets = []
        for player in self.players:
            player.set_strategy_set(self.resources)
            strategy_sets.append(player.get_strategy_set())
        self.strategy_profiles = list(itertools.product(*strategy_sets))

    def get_strategy_profiles(self):
        try:
            return self.strategy_profiles
        except:
            print("Strategy profiles have not been defined.")

    def calculate_utility(self):
        print(f'Choose a strategy of Player from below')
        for i in range(len(self.players)):
            print(f'{i}: Player {self.players[i].get_id()}')
        index = input('Enter number: ')
        player = self.players[int(index)]
        congestion, choices = self.selector()
        probability_product = 1
        total_cost = 0
        for resource in choices[player][1]:
            failure_probability = resource.get_failure_probability(congestion[resource]-1)
            cost = resource.get_cost(congestion[resource]-1)
            probability_product *= failure_probability
            total_cost += cost
            #print(resource.get_id())
            #print(probability_product)
            #print(total_cost)

        utility = player.get_benefit()*(1-probability_product) - total_cost
        return utility

    def selector(self):
        # calculate congestion here
        congestion = {key: 0 for key in self.resources}
        choices = {key: 0 for key in self.players}
        for player in self.players:
            print(f'Choose a strategy of Player {player.get_id()} from below')
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
            print(f'{number} chosen')
            index = int(number)
            print(strategy_set[index][1])
            for resource in strategy_set[index][1]:
                congestion[resource] += 1
            choices[player] = strategy_set[index]
        for resource in self.resources:
            print(f'Congestion of {resource.get_id()}: {congestion[resource]}')
        return (congestion, choices)