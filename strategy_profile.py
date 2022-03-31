from copy import deepcopy

from player import Player
from resource import Resource

from typing import Dict, Set

class StrategyProfile():
    def __init__(self, strategies: Dict[int, Set[int]], players: Dict[int, Player], resources: Dict[int, Resource]):
        self.strategies = strategies # key: player id, value: a set of int(resource id)
        self.players = players
        self.resources = resources
        self.utilities: Dict[int, float] = dict() # key: player_id, value: float
        self.congestion = None
        self.even = None
        self.social_utility = None
        self.update_profile()

    def update_profile(self):
        self.congestion = self.get_congestion(self.strategies)
        self.even = self.check_even()
        self.calculate_utilities()
        self.social_utility = sum(self.utilities.values())

    def check_even(self) -> int:
        congestions = set()
        for congestion in self.congestion.values():
            congestions.add(congestion)
        if len(congestions) == 1:
            return congestions.pop()
        else:
            return None

    def get_utilities(self) -> Dict[int, float]:
        return self.utilities

    def get_strategies(self) -> Dict[int, Set[int]]:
        return self.strategies

    def get_utility(self, player_id) -> float:
        # exception handling
        return self.utilities[player_id]

    def get_congestion(self, strategies: Dict[int, Set[int]]) -> Dict[int, int]:
        congestion = {key: 0 for key in self.resources.keys()} # key: resource, value: int
        for strategy in strategies.values():
            for resource in strategy:
                congestion[resource] += 1
        return congestion

    def update_congestion(self):
        self.congestion = self.get_congestion(self.strategies)

    def simulate_change(self, strategy: set, player_id) -> bool:
        new_strategies = deepcopy(self.strategies)
        new_strategies[player_id] = strategy
        new_congestion = self.get_congestion(new_strategies)
        return self.calculate_utility(player_id, strategy, new_congestion) > self.utilities[player_id]

    def calculate_utility(self, player, strategy, congestion) -> float:
        probability_product = 1 # if player didnt choose any resource, failure probability = 1
        total_cost = 0
        for resource in strategy:
            failure_probability = self.resources[resource].get_failure_probability(congestion[resource])
            cost = self.resources[resource].get_cost(congestion[resource])
            probability_product *= failure_probability
            total_cost += cost
        return self.players[player].get_benefit()*(1-probability_product) - total_cost

    def calculate_utilities(self):
        for player_id, strategy in self.strategies.items():
            self.utilities[player_id] = self.calculate_utility(player_id, strategy, self.congestion)

    def display_result(self):
        print(f'Number of players: {len(self.players.keys())}')
        print(f'Social Utility: {self.social_utility}')
        print(f'Resource Cost: {self.resources[1].costs}')
        print(f'Resource Failure Probability: {self.resources[1].failure_probabilities}')
        print()
        for player in self.players.keys():
            print(f'Player {player}')
            print(f'Benefit: {self.players[player].benefit}')
            print(f'Strategy: {self.strategies[player]}')
            print(f'Utility: {self.utilities[player]}')
            print()
            print()