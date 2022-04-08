from copy import deepcopy

from player import Player
from resource import Resource

from typing import Dict, Set

class StrategyProfile():

    def __init__(self, strategies: Dict[int, Set[int]], players: Dict[int, Player], resources: Dict[int, Resource]):
        """
        Constructor that gets run when CGLF class construct strategy profiles or equilibrium profile is constructed
        
        Parameters
        ----------
        players : Dict[int, Player]
            a set of players in a game

        resources : Dict[int, Resource]
            a set of resources to be used by players in a game
        """

        self.__strategies: Dict[int, Set[int]] = strategies # key: player_id, value: a set of int(resource id)
        self.__players: Dict[int, Player] = players
        self.__resources: Dict[int, Resource] = resources
        self.__utilities: Dict[int, float] = dict() # key: player_id, value: float
        self.__congestion: Dict[int, int] = dict()
        self.__even: int = None
        self.__social_utility: float = None
        self.update_profile()

    def update_profile(self):
        """
        Update member variables
        """

        self.__congestion = self.calculate_congestion(self.__strategies)
        self.__even = self.check_even()
        self.calculate_utilities()
        self.__social_utility = sum(self.__utilities.values())

    def check_even(self) -> int:
        """
        Check whether this strategy profile's resouces are evenly assigned to players

        Returns
        -------
        congestion : int
            common congestion number
        """

        congestions = set()
        for congestion in self.__congestion.values():
            congestions.add(congestion)
        if len(congestions) == 1:
            return congestions.pop()
        else:
            return None

    def get_utilities(self) -> Dict[int, float]:
        """
        Return a member variable of utilities of all players

        Returns
        -------
        utilities : Dict[int, float]
            utilities of all players, key: player_id, value: utility value
        """

        return self.__utilities

    def get_strategies(self) -> Dict[int, Set[int]]:
        """
        Return a member variable of strategies of all players

        Returns
        -------
        strategies : Dict[int, Set[int]]
            strategies of all players, key: player_id, value: set of resource_id
        """

        return self.__strategies

    def get_utility(self, player_id) -> float:
        """
        Return a member variable of utility of player
        
        Parameters
        ----------
        player_id : int
            player's id 

        Returns
        -------
        utility : float
            player's utility
        """

        return self.__utilities[player_id]

    def get_social_utility(self) -> float:
        """
        Return a member variable of social_utility

        Returns
        -------
        social_utility : float
            social utility of this strategy profile
        """

        return self.__social_utility

    def get_congestion(self) -> Dict[int, int]:
        """
        Return a member variable of congestion

        Returns
        -------
        congestion : Dict[int, int]
            a dict of congestion (key: resource_id, value: amount of congestion)
        """

        return self.__congestion

    def calculate_congestion(self, strategies: Dict[int, Set[int]]) -> Dict[int, int]:
        """
        Calculate congestion given strategies of all players
        
        Parameters
        ----------
        strategies : Dict[int, Set[int]]
            strategies of all players, key: player_id, value: set of resource_id

        Returns
        -------
        congestion : Dict[int, int]
            congestion, key: resource_id, congestion
        """

        congestion = {key: 0 for key in self.__resources.keys()} # key: resource_id, value: int
        for strategy in strategies.values():
            for resource in strategy:
                congestion[resource] += 1
        return congestion

    def simulate_change(self, strategy: Set[int], player_id: int) -> bool:
        """
        Simulate the if a given player change to another strategy in this profile
        
        Parameters
        ----------
        strategy : Set[int]
            a set of resources to be used by players in a game

        player_id : int
            player's id

        Returns
        -------
        strategy_set : bool
            Return true if the change is beneficial to the player; otherwise, false
        """

        new_strategies = deepcopy(self.__strategies)
        new_strategies[player_id] = strategy
        new_congestion = self.calculate_congestion(new_strategies)
        return self.calculate_utility(player_id, strategy, new_congestion) > self.__utilities[player_id]

    def calculate_utility(self, player_id: int, strategy: Set[int], congestion: Dict[int, int]) -> float:
        """
        Calculate a utility of a given player
        
        Parameters
        ----------
        player_id : int
            player's id
        
        strategy : Set[int]
            player's strategy

        congestion : Dict[int, int]
            congestion of a strategy profile

        Returns
        -------
        strategy_set : float
            player's utility
        """

        probability_product = 1 # if player didn't choose any resource, failure probability = 1
        total_cost = 0
        for resource in strategy:
            failure_probability = self.__resources[resource].get_failure_probability(congestion[resource])
            cost = self.__resources[resource].get_cost(congestion[resource])
            probability_product *= failure_probability
            total_cost += cost
        return self.__players[player_id].get_benefit()*(1-probability_product) - total_cost

    def calculate_utilities(self):
        """
        Calculate utilities of all players
        """

        for player_id, strategy in self.__strategies.items():
            self.__utilities[player_id] = self.calculate_utility(player_id, strategy, self.__congestion)

    def display_result(self):
        """
        Print the information of this strategy profile
        """

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