from resource import Resource
from player import Player
from cglf import CGLF
from equilibrium import Equilibrium
from strategy_profile import StrategyProfile
import random

import openpyxl

from typing import Dict

from copy import deepcopy

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def validation(num_players, num_resources, benefit, start_cost):
    if num_players < 2 or num_players > 10:
        print(f'The number of players must be more than 1 and less than 11.')
        return False
    if num_resources < 2 or num_resources > 10:
        print(f'The number of players must be more than 1 and less than 11.')
        return False
    if benefit < 0:
        print(f'Benefit must be non-negative number.')
        return False
    if start_cost < 0:
        print(f'Cost must be non-negative number.')
        return False
    return True

def enter_variables():
    try:
        num_players = int(input('Enter the number of players in integer: '))
        num_resources = int(input('Enter the number of resources in integer: '))
        benefit = float(input('Enter the value of benefit: '))
        start_cost = float(input('Enter the value of initial cost for resource: '))
        start_fp = float(input('Enter the value of initial failure probability for resource: '))
        print("Success")
    except:
        print("Enter value in correct data type")

def price_of_anarchy_v0(num_players, num_resources, benefit, start_cost, start_probability):
    if not validation(num_players, num_resources, benefit, start_cost):
        return False
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
    equilibrium_profile: StrategyProfile = Equilibrium(players, resources).profile
    print(f'Equilibrium utility: {equilibrium_profile.social_utility}')

#price_of_anarchy_v0(1000,100,10,1,1)

def price_of_anarchy_v1_1():
    try:
        num_players = int(input('Enter the number of players in integer: '))
        if num_players < 2 or num_players > 10:
            print(f'The number of players must be more than 1 and less than 11.')
            return False
        num_resources = int(input('Enter the number of resources in integer: '))
        if num_resources < 2 or num_resources > 10:
            print(f'The number of players must be more than 1 and less than 11.')
            return False
        if num_players >= 5 and num_resources >= 5:
            print(f'The number of players and resources cannot be more than 4 at the same time')
            return False
        benefit = float(input('Enter the value of benefit: '))
        if benefit < 0:
            print(f'Benefit must be non-negative number.')
            return False
        start_cost = float(input('Enter the value of initial cost for resource: '))
        if start_cost < 0:
            print(f'Cost must be non-negative number.')
            return False
        start_probability = float(input('Enter the value of initial failure probability for resource: '))

        players = dict()
        initial_benefit = benefit
        initial_cost = start_cost
        initial_fail = 1 - 1 / (1 + 1 / 10 * start_probability)
        for i in range(1, num_players + 1):
            players[i] = Player(i, benefit)
            #benefit /= 5
            benefit = i ** i + initial_benefit
        cost = dict()
        failure_probability = dict()
        for i in range(1, num_players + 1):
            failure_probability[i] = 1 - 1 / (1 + i / 10 * start_probability)
        for i in range(1, num_players + 1):
            #cost[i] = i ** i + start_cost
            cost[i] = i * start_cost
        resources: Dict[int, Resource] = dict()
        for i in range(1, num_resources + 1):
            resources[i] = Resource(i, cost, failure_probability)
        cglf = CGLF(players, resources)
        optimal_profile: StrategyProfile = max(cglf.strategy_profiles, key=lambda x:x.social_utility)
        equilibrium_profile: StrategyProfile = Equilibrium(players, resources).profile
        social_optima: float = optimal_profile.social_utility
        if int(equilibrium_profile.social_utility) != 0:
            price_of_anarchy = social_optima / equilibrium_profile.social_utility
            #print(f'Price of Anarchy: {social_optima / equilibrium_profile.social_utility}')
            return (benefit, initial_cost, price_of_anarchy)
        else:
            #print(f'Equilibrium utility: {equilibrium_profile.social_utility}')
            return (benefit, initial_cost, 0)
        
    except:
        print("Enter value in correct data type")
""" for player in range(2, 11):
    print(price_of_anarchy_v1(player,2,100,1,1)) """

# dataset_1_1 = [[price_of_anarchy_v1_1(2,2,benefit,cost,1) for benefit in range(0,101, 10)] for cost in range(0,11)]
# print(price_of_anarchy_v1_1())

def price_of_anarchy_v1_2(num_players, num_resources, benefit, start_cost, start_probability):
    if not validation(num_players, num_resources, benefit, start_cost):
        return False

    """ print(f'Num of players: {num_players}')
    print(f'Num of resources: {num_resources}')
    print(f'Initial benefit: {benefit}')
    print(f'Initial cost: {start_cost}')
    print(f'Initial failure probability: {start_probability}') """

    players = dict()
    initial_benefit = benefit
    initial_cost = start_cost
    initial_fail = 1 - 1 / (1 + 1 / 10 * start_probability)
    for i in range(1, num_players + 1):
        players[i] = Player(i, benefit)
        benefit = initial_benefit - (i + 1) ** 2
    failure_probability = dict()
    for i in range(1, num_players + 1):
        failure_probability[i] = 1 - 1 / (1 + i / 10 * start_probability)
    cost = dict()
    for i in range(1, num_players + 1):
        cost[i] = i * (start_cost + 1)
    resources: Dict[int, Resource] = dict()
    for i in range(1, num_resources + 1):
        resources[i] = Resource(i, cost, failure_probability)
    cglf = CGLF(players, resources)
    optimal_profile: StrategyProfile = max(cglf.strategy_profiles, key=lambda x:x.social_utility)
    equilibrium_profile: StrategyProfile = Equilibrium(players, resources).profile
    social_optima: float = optimal_profile.social_utility
    if int(equilibrium_profile.social_utility) != 0:
        price_of_anarchy = social_optima / equilibrium_profile.social_utility
        #print(f'Price of Anarchy: {social_optima / equilibrium_profile.social_utility}')
        #return (initial_benefit, initial_cost, price_of_anarchy)
        return price_of_anarchy
    else:
        #print(f'Equilibrium utility: {equilibrium_profile.social_utility}')
        #return (initial_benefit, initial_cost, None)
        return None

dataset_1_2 = [[price_of_anarchy_v1_2(player,resource,100,5,5) for resource in range(2,5)] for player in range(2,5)]
#enter_variables()
#print(price_of_anarchy_v1_2(4,4,100,1,1))

def check_algorithm(num_players, num_resources, benefit, start_cost, start_probability):
    if not validation(num_players, num_resources, benefit, start_cost):
        return False
    players = dict()
    initial_benefit = benefit
    initial_cost = start_cost
    initial_fail = 1 - 1 / (1 + 1 / 10 * start_probability)
    for i in range(1, num_players + 1):
        players[i] = Player(i, benefit)
        #benefit /= 5
        benefit = initial_benefit - (i + 1) ** 2
    cost = dict()
    failure_probability = dict()
    for i in range(1, num_players + 1):
        failure_probability[i] = 1 - 1 / (1 + i / 10 * start_probability)
    for i in range(1, num_players + 1):
        #cost[i] = i ** i + start_cost
        cost[i] = i * (start_cost + 1)
    resources: Dict[int, Resource] = dict()
    for i in range(1, num_resources + 1):
        resources[i] = Resource(i, cost, failure_probability)
    cglf = CGLF(players, resources)
    optimal_profile: StrategyProfile = max(cglf.strategy_profiles, key=lambda x:x.social_utility)
    optimal_profile.display_result()
    #cglf.display_all()
    equilibrium_profile: StrategyProfile = Equilibrium(players, resources).profile
    equilibrium_profile.display_result()
    print(optimal_profile.social_utility/equilibrium_profile.social_utility)
    

#check_algorithm(3, 5, 100,5,0) #finish at step4 worked probably correctly
#check_algorithm(4, 4, 100,8,10)
""" for i in range(2,11):
    check_algorithm(i, 2, 10,1,1) """

def export_excel_2d(data):
    wb = openpyxl.Workbook()

    # Check Sheet
    print(f'Sheet name: {wb.get_sheet_names()}')

    # Retrieve sheet object
    s1 = wb.get_sheet_by_name(wb.get_sheet_names()[0])

    for i in range(len(data)):
        for j in range(len(data[i])):
            s1.cell(row=i+1,column=j+1,value=data[i][j])

    wb.save('test.xlsx')

""" def graph(data):
    tX = []
    tY = []
    tz = []
    for element in data:
        tX.append(element[0])
        tY.append(element[1])
        tz.append(element[2])
    TX= np.array(tX)
    TY= np.array(tY)
    TZ= np.array(tz)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.set_title("Tmp", size=20)
    ax.set_xlabel('x', size=15, color='black')
    ax.set_ylabel('y', size=15, color='black')
    ax.set_zlabel('z', size=15, color='black')
    print(TX)

    ax.plot_wireframe(TX,TY,TZ)
    plt.show() """

# graph(dataset_1_1)

""" def export_excel_3d(data):
    wb = openpyxl.Workbook()

    # Check Sheet
    print(f'Sheet name: {wb.get_sheet_names()}')

    # Retrieve sheet object
    s1 = wb.get_sheet_by_name(wb.get_sheet_names()[0])

    for i in range(len(data)):
        for j in range(len(data[i])):
            s1.cell(row=i+1,column=j+1,value=data[i][j])

    wb.save('test.xlsx') """

export_excel_2d(dataset_1_2)