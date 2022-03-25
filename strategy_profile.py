# from typing import Optional
from copy import deepcopy

class StrategyProfile():
    def __init__(self, strategies: dict, players, resources):
        self.strategies = strategies # key: player id, value: a set of int(resource id)
        self.players = players
        self.resources = resources
        #self.congestion = None # key: resource_id, value: int
        self.utilities = dict() # key: player_id, value: float
        self.congestion = self.get_congestion(self.strategies) # key: int(resource id), value: int
        self.even = self.check_even()
        self.calculate_utilities()

    def check_even(self) -> int:
        congestions = set()
        for congestion in self.congestion.values():
            congestions.add(congestion)
        if len(congestions) == 1:
            return congestions.pop()
        else:
            return None

    def get_utilities(self):
        return self.utilities

    def get_strategies(self):
        return self.strategies

    def get_utility(self, player_id) -> float:
        # exception handling
        return self.utilities[player_id]

    def get_congestion(self, strategies):
        congestion = {key: 0 for key in self.resources.keys()} # key: resource, value: int
        for strategy in strategies.values():
            for resource in strategy:
                congestion[resource] += 1
        return congestion

    def simulate_change(self, strategy: set, player_id) -> bool:
        new_strategies = deepcopy(self.strategies)
        new_strategies[player_id] = strategy
        new_congestion = self.get_congestion(new_strategies)
        return self.calculate_utility(player_id, strategy, new_congestion) > self.utilities[player_id]

    def calculate_utilities(self):
        for player_id, strategy in self.strategies.items():
            self.utilities[player_id] = self.calculate_utility(player_id, strategy, self.congestion)

    def calculate_utility(self, player, strategy, congestion):
        probability_product = 1 # if player didnt choose any resource, failure probability = 1
        total_cost = 0
        for resource in strategy:
            failure_probability = self.resources[resource].get_failure_probability(congestion[resource])
            cost = self.resources[resource].get_cost(congestion[resource])
            probability_product *= failure_probability
            total_cost += cost
        return self.players[player].get_benefit()*(1-probability_product) - total_cost

    def display_result(self):
        print(f'Number of players: {len(self.players.keys())}')
        for player in self.players.keys():
            print(f'Player {player}')
            print(f'Strategy: {self.strategies[player]}')
            print(f'Utility: {self.utilities[player]}')
            print()

    def display_all_info(self):
        print(f'{self.strategies}')