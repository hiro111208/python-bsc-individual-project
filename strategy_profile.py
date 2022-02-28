class StrategyProfile():
    def __init__(self, players):
        self.players = players
        self.congestion = dict()
        self.utilities = dict()

    def get_utilities(self):
        return self.utilities

    def get_players(self):
        return self.players

    def get_congestion(self, strategy_profile): # strategy profile is dict of 
        congestion = {key: 0 for key in self.resources}
        for element in strategy_profile.values():
            for resource in element:
                congestion[resource] += 1
        return congestion

    def set_congestion(self):
        congestion = dict()
        for player in self.players:
            for resource in player.strategy:
                if resource not in congestion:
                    congestion[resource] = 1
                else:
                    congestion[resource] += 1
        self.congestion = congestion

    def get_utility(self):
        choices = {key: None for key in self.players} # dict key: player, value: player's strategy
        print(f'Choose Player from below')
        for i in range(len(self.players)):
            print(f'{i}: Player {self.players[i].get_id()}')
        index = input('Enter number: ')
        target_player = self.players[int(index)]
        for player in self.players:
            print(f'Choose a strategy of Player {target_player.get_id()} from below')
            for i in range(len(self.strategy_set)):
                resource_id = ""
                if self.strategy_set[i] == []:
                    resource_id = "Empty"
                else:
                    for resource in self.strategy_set[i]:
                        resource_id += (resource.get_id() + " ")
                print(f'{i}: {resource_id}')
            number = input('Enter number: ') # must be below the length of resources
            index = int(number)
            #print(len(strategy_profiles))
            #strategy_profiles = list(filter(lambda strategy_profile: (strategy_set[index]) in list(strategy_profile[0]), strategy_profiles))
            #print(len(strategy_profiles))
            choices[player] = self.strategy_set[index]
        for cell in self.pay_off_matrix:
            if choices == cell['strategy_profile']:
                return cell['utilities'][target_player]

    def calculate_utility(self, player, congestion):
        # strategy is a list of resources
        probability_product = 1
        total_cost = 0
        for resource in player.strategy:
            failure_probability = resource.get_failure_probability(self.congestion[resource]-1)
            cost = resource.get_cost(self.congestion[resource]-1)
            probability_product *= failure_probability
            total_cost += cost
        utility = player.get_benefit()*(1-probability_product) - total_cost
        return utility

    def calculate_utilities(self):
        for player in self.players:
            probability_product = 1
            total_cost = 0
            for resource in player.strategy:
                failure_probability = resource.get_failure_probability(self.congestion[resource]-1)
                cost = resource.get_cost(self.congestion[resource]-1)
                probability_product *= failure_probability
                total_cost += cost
            utility = player.get_benefit()*(1-probability_product) - total_cost
            self.utilities[player] = utility
        self.pay_off_matrix.append({'strategy_profile':strategy_profile, 'utilities':utilities})