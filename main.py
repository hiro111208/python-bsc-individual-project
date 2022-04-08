from resource import Resource
from player import Player
from cglf import CGLF
from equilibrium import Equilibrium
from strategy_profile import StrategyProfile
from typing import Dict

import openpyxl


def validation(num_players, num_resources, benefit, start_cost, start_probability):
    if not type(num_players) == int or (num_players < 2 or num_players > 10):
        print(f'The number of players must be more than 1 and less than 11.')
        return False
    if not type(num_resources) == int or (num_resources < 2 or num_resources > 10):
        print(f'The number of players must be more than 1 and less than 11.')
        return False
    if not type(benefit) == int or benefit < 0:
        print(f'Benefit must be non-negative number.')
        return False
    if not type(start_cost) == int or start_cost < 0:
        print(f'Cost must be non-negative number.')
        return False
    if not type(start_probability) == int:
        return False
    return True

def check_algorithm(num_players, num_resources, benefit, start_cost, start_probability):
    """
    Check whether the software compute a correct Nash equilibrium
    
    Parameters
    ----------
    num_players : int
        the number of players for this game

    num_resources : int
        the number of resources for this game

    benefit : int
        initial player's benefit for this game

    start_cost : int
        initial cost of resource for this game

    start_probability : int
        initial failure probability of resource for this game
    """

    if not validation(num_players, num_resources, benefit, start_cost, start_probability):
        return False
    players = dict()
    initial_benefit = benefit
    for i in range(1, num_players + 1):
        players[i] = Player(i, benefit)
        benefit = initial_benefit - (i + 1) ** 2
    failure_probability = dict()
    for i in range(1, num_players + 1):
        failure_probability[i] = 1 - 1 / (1 + i / 10 * start_probability)
    cost = dict()
    for i in range(1, num_players + 1):
        cost[i] = i * (start_cost)
    resources: Dict[int, Resource] = dict()
    for i in range(1, num_resources + 1):
        resources[i] = Resource(i, cost, failure_probability)
    cglf = CGLF(players, resources)
    optimal_profile: StrategyProfile = cglf.get_optimal_profile()
    optimal_profile.display_result()
    #cglf.display_all()
    equilibrium_profile: StrategyProfile = Equilibrium(players, resources).get_equilibrium_profile()
    equilibrium_profile.display_result()
    print(optimal_profile.get_social_utility()/equilibrium_profile.get_social_utility())

def calculate_ratio(num_players, num_resources, benefit, start_cost, start_probability):
    """
    Calculate the ratio between social utilities of an obtained Nash equilibrium and 
    the optimal solution of this game
    
    Parameters
    ----------
    num_players : int
        the number of players for this game

    num_resources : int
        the number of resources for this game

    benefit : int
        initial player's benefit for this game

    start_cost : int
        initial cost of resource for this game

    start_probability : int
        initial failure probability of resource for this game

    Returns
    -------
    ratio : float
        inefficiency of an obtained Nash equilibrium of this game
    """

    if not validation(num_players, num_resources, benefit, start_cost, start_probability):
        return False

    players = dict()
    initial_benefit = benefit
    for i in range(1, num_players + 1):
        players[i] = Player(i, benefit)
        benefit = initial_benefit - (i + 1) ** 2
    failure_probability = dict()
    for i in range(1, num_players + 1):
        failure_probability[i] = 1 - 1 / (1 + i / 10 * start_probability)
    cost = dict()
    for i in range(1, num_players + 1):
        cost[i] = i * (start_cost)
    resources: Dict[int, Resource] = dict()
    for i in range(1, num_resources + 1):
        resources[i] = Resource(i, cost, failure_probability)
    cglf = CGLF(players, resources)
    optimal_profile: StrategyProfile = cglf.get_optimal_profile()
    equilibrium_profile: StrategyProfile = Equilibrium(players, resources).get_equilibrium_profile()
    social_optima: float = optimal_profile.get_social_utility()
    if int(equilibrium_profile.get_social_utility()) != 0:
        ratio = social_optima / equilibrium_profile.get_social_utility()
        return ratio
    else:
        print("The social utility of the optimal solution was 0. The ratio was not calculated.")
        return None

# Code modified from https://himibrog.com/python-output-excel/
def export_excel_2d(data, index):
    """
    Export an Excel file given an input
    
    Parameters
    ----------
    data : List[List[float]]
        a set of data

    index : int
        used for naming a file
    """

    wb = openpyxl.Workbook()

    # Check Sheet
    print(f'Sheet name: {wb.get_sheet_names()}')

    # Retrieve sheet object
    s1 = wb.get_sheet_by_name(wb.get_sheet_names()[0])

    for i in range(len(data)):
        for j in range(len(data[i])):
            s1.cell(row=i+1,column=j+1,value=data[i][j])

    wb.save(f'data_{index}_.xlsx')

#check_algorithm(4, 4, 1000,10,5)

data_player_resource = [[calculate_ratio(player,resource,100,5,5) for resource in range(2,5)] for player in range(2,5)]
data_benefit_fp = [[calculate_ratio(4,4,benefit,5,fp) for fp in range(0,11)] for benefit in range(70,171,10)]
data_cost_fp = [[calculate_ratio(4,4,100,cost,fp) for fp in range(0,11)] for cost in range(0,11)]
data_benefit_cost = [[calculate_ratio(4,4,benefit,cost,5) for cost in range(0,11)] for benefit in range(70,171,10)]

dataset = [data_player_resource, data_benefit_fp, data_cost_fp, data_benefit_cost]

for i in range(len(dataset)):
    export_excel_2d(dataset[i], i)