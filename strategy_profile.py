from copy import deepcopy

from player import Player
from resource import Resource

from typing import Dict, Set

class StrategyProfile():
    def __init__(self, strategies: Dict[int, Set[int]], players: Dict[int, Player], resources: Dict[int, Resource]):
        self.__strategies: Dict[int, Set[int]] = strategies # key: player id, value: a set of int(resource id)
        self.__players: Dict[int, Player] = players
        self.__resources: Dict[int, Resource] = resources
        self.__utilities: Dict[int, float] = dict() # key: player_id, value: float
        self.__congestion: Dict[int, int] = None
        self.__even: int = None
        self.__social_utility: float = None
        self.update_profile()

    def update_profile(self):
        self.__congestion = self.calculate_congestion(self.__strategies)
        self.__even = self.check_even()
        self.calculate_utilities()
        self.__social_utility = sum(self.__utilities.values())

    def check_even(self) -> int:
        congestions = set()
        for congestion in self.__congestion.values():
            congestions.add(congestion)
        if len(congestions) == 1:
            return congestions.pop()
        else:
            return None

    def get_utilities(self) -> Dict[int, float]:
        return self.__utilities

    def get_strategies(self) -> Dict[int, Set[int]]:
        return self.__strategies

    def get_utility(self, player_id) -> float:
        # exception handling
        return self.__utilities[player_id]

    def get_social_utility(self) -> float:
        return self.__social_utility

    def get_congestion(self) -> Dict[int, int]:
        return self.__congestion

    def calculate_congestion(self, strategies: Dict[int, Set[int]]) -> Dict[int, int]:
        congestion = {key: 0 for key in self.__resources.keys()} # key: resource, value: int
        for strategy in strategies.values():
            for resource in strategy:
                congestion[resource] += 1
        return congestion

    def update_congestion(self):
        self.__congestion = self.calculate_congestion(self.__strategies)

    def simulate_change(self, strategy: set, player_id) -> bool:
        new_strategies = deepcopy(self.__strategies)
        new_strategies[player_id] = strategy
        new_congestion = self.calculate_congestion(new_strategies)
        return self.calculate_utility(player_id, strategy, new_congestion) > self.__utilities[player_id]

    def calculate_utility(self, player_id, strategy, congestion) -> float:
        probability_product = 1 # if player didnt choose any resource, failure probability = 1
        total_cost = 0
        for resource in strategy:
            failure_probability = self.__resources[resource].get_failure_probability(congestion[resource])
            cost = self.__resources[resource].get_cost(congestion[resource])
            probability_product *= failure_probability
            total_cost += cost
        return self.__players[player_id].get_benefit()*(1-probability_product) - total_cost

    def calculate_utilities(self):
        for player_id, strategy in self.__strategies.items():
            self.__utilities[player_id] = self.calculate_utility(player_id, strategy, self.__congestion)

    def display_result(self):
        print(f'Number of players: {len(self.__players.keys())}')
        print(f'Social Utility: {self.__social_utility}')
        print(f'Resource Cost: {self.__resources[1].get_costs()}')
        print(f'Resource Failure Probability: {self.__resources[1].get_failure_probabilities()}')
        print()
        for player_id in self.__players.keys():
            print(f'Player {player_id}')
            print(f'Benefit: {self.__players[player_id].get_benefit()}')
            print(f'Strategy: {self.__strategies[player_id]}')
            print(f'Utility: {self.__utilities[player_id]}')
            print()
            print()