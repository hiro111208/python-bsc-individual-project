import itertools
import copy
from strategy_profile import StrategyProfile
import collections
from typing import Dict, List, Set
from player import Player
from resource import Resource


class CGLF():

    def __init__(self, players: Dict[int, Player], resources: Dict[int, Resource]):
        self.players = players # key:int, value:Player
        """ self.players = dict()
        for i in range(len(players)):
            self.players[i] = players[i] """
        self.resources = resources # key:int, value:Resource
        """ self.resources = dict()
        for i in range(len(resources)):
            self.resources[i] = resources[i] """
        self.number_of_profiles = 0
        
        self.strategy_set: List[Set[Resource]] = self.set_strategy_set(resources)
        self.strategy_profiles = list()

        self.build_strategy_profiles()

    
    def set_strategy_set(self, resources: Dict[int, Resource]) -> List[Set[Resource]]: # strategies that player can choose
        strategy_set = []
        for i in range(len(resources)+1):
            for strategy in itertools.combinations(resources, i):
                strategy_set.append(set(list(strategy)))
        return strategy_set

    def build_strategy_profiles(self):
        strategy_sets = dict()
        for player in self.players.values():
            strategy_sets[player.id] = self.strategy_set
        product = [x for x in itertools.product(*strategy_sets.values())]
        strategy_profiles = [dict(zip(strategy_sets.keys(), r)) for r in product]
        for strategy_profile in strategy_profiles:
            self.strategy_profiles.append(StrategyProfile(strategy_profile, self.players, self.resources))

    def get_utility(self):
        choices = {key: None for key in self.players} # dict key: player, value: player's strategy
        print(f'Choose Player from below')
        players: List[Player] = list(self.players.values())
        for i in range(len(players)):
            print(f'{i}: Player {players[i].get_id()}')
        index = input('Enter number: ')
        target_player: int = players[int(index)].id
        print(f'Target player chosen: {target_player}')
        for player in players:
            print(f'{player.get_id()} is in a set: {player in self.players}')
            print(f'Choose a strategy of Player {player.get_id()} from below')
            for i in range(len(self.strategy_set)):
                resource_name = ""
                if self.strategy_set[i] == set():
                    resource_name = "Empty"
                else:
                    for resource in self.strategy_set[i]:
                        resource_name += (f'e{resource} ')
                print(f'{i}: {resource_name}')
            number = input('Enter number: ') # must be below the length of resources
            index: int = int(number)
            #print(len(self.strategy_profiles))
            choices[player.id]: Set[int] = self.strategy_set[index]
        # print(f'choices: {choices}')
        for strategy_profile in self.strategy_profiles:
            equality = []
            for player in strategy_profile.strategies.keys(): # strategy is supposed to be set
                equality.append(strategy_profile.strategies[player]==choices[player])
            # print(f'equality: {equality}')
            if set(equality) == {True}:
                print(f'even: {strategy_profile.even}')
                return strategy_profile.utilities[target_player]

    def display(self):
        for sp in self.strategy_profiles:
            if sp.even != None:
                print(f'{sp.even}-even')
                for player in self.players.values():
                    print(f'Player {player.id}: {sp.utilities[player.id]}')
                print()

    def display_all(self):
        for sp in self.strategy_profiles:
            for player_id in sp.players.keys():
                print(f'Player {player_id}')
                print(f'Resource: {sp.strategies[player_id]}')
                print(f'Utility: {sp.utilities[player_id]}')
                print()
            print()
            print()