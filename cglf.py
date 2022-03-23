import itertools
import copy
from strategy_profile import StrategyProfile
import collections


class CGLF():

    def __init__(self, players: dict, resources):
        self.players = players # key:int, value:Player
        """ self.players = dict()
        for i in range(len(players)):
            self.players[i] = players[i] """
        self.resources = resources # key:int, value:Resource
        """ self.resources = dict()
        for i in range(len(resources)):
            self.resources[i] = resources[i] """
        self.number_of_profiles = 0
        
        self.strategy_set = self.set_strategy_set(resources)
        self.strategy_profiles = list()

        self.build_strategy_profiles()

    
    def set_strategy_set(self, resources): # strategies that player can choose
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

    """ def build_strategy_profiles(self):
        strategy_sets = dict()
        for player in self.players:
            # player.set_strategy_set(self.resources)
            # strategy_sets[player] = player.get_strategy_set()
            strategy_sets[player] = self.strategy_set
        strategy_profiles = itertools.product(strategy_sets, len(self.players))
        for strategy_profile in strategy_profiles:
            self.strategy_profiles.append(sp.StrategyProfile(strategy_profile, self.players, self.resources)) """

    def get_utility(self):
        choices = {key: None for key in self.players} # dict key: player, value: player's strategy
        print(f'Choose Player from below')
        players = list(self.players)
        for i in range(len(players)):
            print(f'{i}: Player {players[i].get_id()}')
        index = input('Enter number: ')
        target_player = players[int(index)]
        print(f'Target player chosen: {target_player.get_id()}')
        for player in players:
            print(f'{player.get_id()} is in a set: {player in self.players}')
            print(f'Choose a strategy of Player {player.get_id()} from below')
            for i in range(len(self.strategy_set)):
                resource_name = ""
                if self.strategy_set[i] == set():
                    resource_name = "Empty"
                else:
                    for resource in self.strategy_set[i]:
                        resource_name += (f'e{resource.get_id()} ')
                print(f'{i}: {resource_name}')
            number = input('Enter number: ') # must be below the length of resources
            index = int(number)
            #print(len(self.strategy_profiles))
            choices[player] = self.strategy_set[index]
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