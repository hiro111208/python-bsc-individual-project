from resource import Resource
from player import Player
from cglf import CGLF
from equilibrium import Equilibrium
from strategy_profile import StrategyProfile
from failure_probability import FailureProbability
from cost import Cost
import random

import openpyxl

from typing import Dict

from copy import deepcopy

# the number of congestions must be equal to the number of players

def price_of_anarchy_v0(num_players, num_resources, benefit, start_cost, start_probability):
    players = dict()
    for i in range(1, num_players + 1):
        players[i] = Player(i, benefit)
        benefit /= 5
    cost = dict()
    failure_probability = dict()
    rand_nums = sorted([random.randint(1, 100) for i in range(len(players))])
    for i in range(1, num_players + 1):
        failure_probability[i] = i / 100
        #failure_probability[i] = 1 - 1 / (1 + i * start_probability)
    for i in range(1, num_players + 1):
        cost[i] = i * start_cost
    resources: Dict[int, Resource] = dict()
    for i in range(1, num_resources + 1):
        resources[i] = Resource(i, cost, failure_probability)
    equilibrium_profile: StrategyProfile = Equilibrium(players, resources)
    print(f'Equilibrium utility: {equilibrium_profile.profile.social_utility}')

#price_of_anarchy_v0(1000,100,10,1,1)

def price_of_anarchy_v1(num_players, num_resources, benefit, start_cost, start_probability):
    players = dict()
    initial_benefit = benefit
    initial_cost = start_cost
    initial_fail = 1 - 1 / (1 + 1 / 10 * start_probability)
    for i in range(1, num_players + 1):
        players[i] = Player(i, benefit)
        benefit /= 5
    cost = dict()
    failure_probability = dict()
    rand_nums = sorted([random.randint(1, 100) for i in range(len(players))])
    for i in range(1, num_players + 1):
        #failure_probability[i] = i*9 / 100
        failure_probability[i] = 1 - 1 / (1 + i / 10 * start_probability)
    for i in range(1, num_players + 1):
        cost[i] = i * start_cost
    resources: Dict[int, Resource] = dict()
    for i in range(1, num_resources + 1):
        resources[i] = Resource(i, cost, failure_probability)
    cglf = CGLF(players, resources)
    #print(cglf.get_utility())
    optimal_profile: StrategyProfile = max(cglf.strategy_profiles, key=lambda x:x.social_utility)
    equilibrium_profile: StrategyProfile = Equilibrium(players, resources)
    social_optima: float = optimal_profile.social_utility
    if social_optima != 0:
        price_of_anarchy = social_optima / equilibrium_profile.profile.social_utility
        #print(f'Price of Anarchy: {social_optima / equilibrium_profile.profile.social_utility}')
        return (initial_fail, price_of_anarchy, social_optima, equilibrium_profile.profile.social_utility)
    else:
        #print(f'Equilibrium utility: {equilibrium_profile.profile.social_utility}')
        return (initial_fail, None, social_optima, equilibrium_profile.profile.social_utility)
""" for player in range(2, 11):
    print(price_of_anarchy_v1(player,2,100,1,1)) """

dataset = [price_of_anarchy_v1(3,3,100,1,fp) for fp in range(0,101)]



def price_of_anarchy_v2(max_players, max_resources, max_benefit, max_cost, max_probability):
    for num_players in range(2, max_players + 1):
        for num_resources in range(2, max_resources + 1):
            for benefit in range(1, max_benefit + 1):
                for start_cost in range(1, max_cost + 1):
                    for start_probability in range(1, max_probability + 1):
                        players = dict()
                        for i in range(1, num_players + 1):
                            players[i] = Player(i, benefit)
                            benefit /= 5
                        cost = dict()
                        failure_probability = dict()
                        rand_nums = sorted([random.randint(1, 100) for i in range(len(players))])
                        for i in range(1, num_players + 1):
                            #failure_probability[i] = rand_nums[i-1] / 100
                            failure_probability[i] = i / 100
                            #failure_probability[i] = 1 - 1 / (1 + i * start_probability)
                        for i in range(1, num_players + 1):
                            cost[i] = i * start_cost
                        resources: Dict[int, Resource] = dict()
                        for i in range(1, num_resources + 1):
                            resources[i] = Resource(i, cost, failure_probability)
                        cglf = CGLF(players, resources)
                        #print(cglf.get_utility())
                        optimal_profile: StrategyProfile = max(cglf.strategy_profiles, key=lambda x:x.social_utility)
                        equilibrium_profile: StrategyProfile = Equilibrium(players, resources)
                        social_optima: float = optimal_profile.social_utility
                        if social_optima != 0:
                            print(f'Price of Anarchy: {social_optima / equilibrium_profile.profile.social_utility}')
                        else:
                            print(f'Equilibrium utility: {equilibrium_profile.profile.social_utility}')
                            """ cglf = CGcglf.display_all()LF(players, resources)
                            cglf.display_all() """
                            #equilibrium_profile.profile.display_result()


#price_of_anarchy_v2(5, 5, 50, 1, 1)

def check_algorithm(num_players, num_resources, benefit):
    players = dict()
    for i in range(1, num_players + 1):
        players[i] = Player(i, benefit)
        benefit /= 5
    cost = dict()
    failure_probability = dict()
    rand_nums = sorted([random.randint(1, 100) for i in range(len(players))])
    for i in range(1, num_players + 1):
        #failure_probability[i] = rand_nums[i-1] / 100
        #failure_probability[i] = 1 - 1 / (1 + i)
        failure_probability[i] = i / 100
    for i in range(1, num_players + 1):
        cost[i] = i
    resources: Dict[int, Resource] = dict()
    for i in range(1, num_resources + 1):
        resources[i] = Resource(i, cost, failure_probability)
    cglf = CGLF(players, resources)
    #cglf.display_all()
    equilibrium_profile: StrategyProfile = Equilibrium(players, resources).profile
    equilibrium_profile.display_result()

#check_algorithm(2, 10, 10)

def export_excel(data):
    wb = openpyxl.Workbook()

    # Check Sheet
    print(f'Sheet name： {wb.get_sheet_names()}')

    # Retrieve sheet object
    s1 = wb.get_sheet_by_name(wb.get_sheet_names()[0])

    for i in range(len(data)):
        for j in range(len(data[i])):
            s1.cell(row=i+1,column=j+1,value=data[i][j])

    wb.save('test.xlsx')

# export_excel(dataset)

""" cost = dict()
failure_probability = dict()
rand_nums = sorted([random.randint(1, 100) for i in range(len(players))])
for i in range(1, number_of_players + 1):
    #failure_probability[i] = rand_nums[i-1] / 100
    failure_probability[i] = i / 100
for i in range(1, number_of_players + 1):
    cost[i] = i*2
resources: Dict[int, Resource] = dict()
for i in range(1, number_of_resources + 1):
    resources[i] = Resource(i, cost, failure_probability)
cglf = CGLF(players, resources)
#print(cglf.get_utility())
optimal_profile: StrategyProfile = max(cglf.strategy_profiles, key=lambda x:x.social_utility)
equilibrium_profile: StrategyProfile = Equilibrium(players, resources)
social_optima: float = optimal_profile.social_utility
print(f'Social optima: {social_optima}')
print(f'Price of Anarchy: {social_optima / equilibrium_profile.profile.social_utility}') """

#print(cglf1.calculate_utility())
#print(cglf1.get_utility())
#print(type(StrategyProfile({1: {1}, 2: {1}}, players, resources)))
# equilibrium_profile = Equilibrium(players, resources).tmp()

""" for i in range(1):
    cost = dict()
    failure_probability = dict()
    rand_nums = sorted([random.randint(1, 99) for i in range(len(players))])
    for i in range(number_of_players):
        # failure_probability[i + 1] = rand_nums[i] / 100
        failure_probability[i + 1] = i + 1 / 100
    for i in range(1, len(players) + 1):
        cost[i] = (i + 5) * 2
    resources = dict()
    for i in range(1, number_of_resources + 1):
        resources[i] = Resource(i, Cost(cost), FailureProbability(failure_probability))
    tmp_strategies = {key:set(random.choices(list(resources.keys()), k=random.randint(1, len(resources)))) for key in players.keys()}

    cglf = CGLF(players, resources)

    
    
    # cglf1.display_all()
    # StrategyProfile(tmp_strategies, players, resources)
    equilibrium_profile = Equilibrium(players, resources)
    print(equilibrium_profile.profile.display_result())
    optimal_profile = max(cglf.strategy_profiles, key=lambda x:x.social_utility)
    social_optima = optimal_profile.social_utility
    print(f'Social optima: {social_optima}')
    print(f'Price of Anarchy: {social_optima / equilibrium_profile.profile.social_utility}') """

""" strategy = {1,2,3}
print(f'strategy {hex(id(strategy))}')
new_strategy = strategy
print(f'new_strategy {hex(id(new_strategy))}')
another_strategy = deepcopy(strategy)
print(f'another_strategy {hex(id(another_strategy))}') """

""" player1 = Player(1,7500)
player2 = Player(2,1500)
player3 = Player(3,150)
player4 = Player(4,150)
player5 = Player(5,150)
player6 = Player(6,150)
player7 = Player(7,15)
players = {player1.id:player1,player2.id:player2,player3.id:player3,player4.id:player4,player5.id:player5,player6.id:player6,player7.id:player7}

cost = {1:9,2:16,3:20,4:30,5:39,6:40,7:50}
failure_probability = {1:0.1,2:0.2,3:0.44,4:0.5,5:0.8,6:0.9,7:0.99}
resources = {key:Resource(key, Cost(cost), FailureProbability(failure_probability)) for key in range(1,9)}
cglf = CGLF(players, resources)
cglf.get_utility() """
""" equilibrium_profile = Equilibrium(players, resources)
print(equilibrium_profile.profile.display_result()) """