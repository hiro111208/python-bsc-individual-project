from resource import Resource
from player import Player
from cglf import CGLF
from equilibrium import Equilibrium
from strategy_profile import StrategyProfile
from failure_probability import FailureProbability
from cost import Cost
from random import randint

# the number of congestions must be equal to the number of players
""" player1 = Player(1, 10)
player2 = Player(2, 5)
player3 = Player(3, 2.5)
players = {player1.id: player1, player2.id:player2} """
players = dict()
number_of_players = 250
# number_of_players = 2
for i in range(1, number_of_players + 1):
    players[i] = Player(i, number_of_players)
    number_of_players -= 1
#player1.set_strategy_set([e1,e2])

number_of_resources = 250
# number_of_resources = 2

""" cost = dict()
failure_probability = dict()
rand_nums = sorted([randint(1, 100) for i in range(len(players))])
for i in range(len(rand_nums)):
    failure_probability[i + 1] = rand_nums[i] / 100
for i in range(1, len(players) + 1):
    cost[i] = i
resources = dict()
number = 2
for i in range(1, number + 1):
    resources[i] = Resource(i, Cost(cost), FailureProbability(failure_probability)) """

#print(cglf1.calculate_utility())
#print(cglf1.get_utility())
#print(type(StrategyProfile({1: {1}, 2: {1}}, players, resources)))
# equilibrium_profile = Equilibrium(players, resources).tmp()
for i in range(1):
    cost = dict()
    failure_probability = dict()
    rand_nums = sorted([randint(1, 99) for i in range(len(players))])
    for i in range(len(rand_nums)):
        failure_probability[i + 1] = rand_nums[i] / 100
    for i in range(1, len(players) + 1):
        cost[i] = i
    resources = dict()
    for i in range(1, number_of_resources + 1):
        resources[i] = Resource(i, Cost(cost), FailureProbability(failure_probability))

    # cglf1 = CGLF(players, resources)
    # cglf1.display_all()
    equilibrium_profile = Equilibrium(players, resources)

    print(equilibrium_profile.profile.display_result())