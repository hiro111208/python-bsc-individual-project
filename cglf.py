import itertools
from strategy_profile import StrategyProfile
from typing import Dict, List, Set
from player import Player
from resource import Resource


class CGLF():

    def __init__(self, players: Dict[int, Player], resources: Dict[int, Resource]):
        """
        Constructor that gets run when main.py is invoked
        
        Parameters
        ----------
        players : Dict[int, Player]
            a set of players in a game

        resources : Dict[int, Resource]
            a set of resources to be used by players in a game
        """

        self.players: Dict[int, Player] = players # key:int, value:Player
        self.resources: Dict[int, Resource] = resources # key:int, value:Resource
        
        self.__strategy_set: List[Set[Resource]] = self.set_strategy_set(resources)
        self.__strategy_profiles: List[StrategyProfile] = self.build_strategy_profiles()
        self.__optimal_profile: StrategyProfile = max(self.__strategy_profiles, key=lambda x:x.get_social_utility())

    
    def set_strategy_set(self, resources: Dict[int, Resource]) -> List[Set[Resource]]: # strategies that player can choose
        """
        Create a strategy set given resources
        
        Parameters
        ----------
        resources : Dict[int, Resource]
            a set of resources to be used by players in a game

        Returns
        -------
        strategy_set : List[Set[Resource]]
            strategy set
        """

        strategy_set = []
        for i in range(len(resources)+1):
            for strategy in itertools.combinations(resources, i):
                strategy_set.append(set(list(strategy)))
        return strategy_set

    def build_strategy_profiles(self) -> List[StrategyProfile]:
        """
        Create strategy profiles given players and resources
        
        Returns
        -------
        strategy_profiles : List[StrategyProfile]
            strategy profiles
        """
        
        strategy_sets = dict()
        for player in self.players.values():
            strategy_sets[player.get_id()] = self.__strategy_set
        product = [x for x in itertools.product(*strategy_sets.values())]
        strategies_set = [dict(zip(strategy_sets.keys(), r)) for r in product]
        strategy_profiles = []
        for strategies in strategies_set:
            strategy_profiles.append(StrategyProfile(strategies, self.players, self.resources))
        return strategy_profiles

    def get_strategy_profiles(self) -> List[StrategyProfile]:
        """
        Return a member variable of strategy profiles
        
        Returns
        -------
        strategy_profiles : List[StrategyProfile]
            strategy profiles
        """

        return self.__strategy_profiles

    def get_optimal_profile(self) -> StrategyProfile:
        """
        Return a member variable of strategy profile
        
        Returns
        -------
        optimal_profile : StrategyProfile
            optimal strategy profile
        """

        return self.__optimal_profile

    def display_all(self):
        """
        Print data of all strategy profiles
        """

        for sp in self.__strategy_profiles:
            for player_id in sp.players.keys():
                print(f'Player {player_id}')
                print(f'Resource: {sp.strategies[player_id]}')
                print(f'Utility: {sp.utilities[player_id]}')
                print()
            print()
            print()