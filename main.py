from resource import Resource
from player import Player
from cglf import CGLF
from equilibrium import Equilibrium

""" e1 = resource.Resource(1)
e2 = resource.Resource(2)
e3 = resource.Resource(3) """
resources = list()
number = 2
for i in range(1, number + 1):
    resources.append(Resource(i, f'e{i}'))

# the number of congestions must be equal to the number of players
player1 = Player(1, 4)
player2 = Player(2, 1.1)
player3 = Player(3, 5)
#player1.set_strategy_set([e1,e2])
""" print(player1.get_strategy_set()[3][1][1].get_id())
print(len(player1.get_strategy_set()))
for i in range(len(player1.get_strategy_set())):
    resource_id = ""
    if player1.get_strategy_set()[i][1] == []:
        resource_id = "Empty"
    else:
        for resource in player1.get_strategy_set()[i][1]:
            resource_id += (resource.get_id() + " ")
    print(resource_id) """

#cglf1 = cglf.CGLF([player1, player2], [e1,e2])
#cglf1 = CGLF([player1, player2], resources)
#print(cglf1.calculate_utility())
print(cglf1.get_utility())
#cglf1.display()
# cglf1.step1()
equilibrium_profile = Equilibrium([player1, player2], resources)
print(equilibrium_profile.display_result())

#print(len(cglf1.get_strategy_profiles()))
#print(cglf1.get_strategy_profiles()[15][0][1][1].get_id())

""" fp1.update_failure_probabilities(0, 0.8)
print(fp1.get_failure_probabilities(0))
fp1.update_failure_probabilities("a", 0.5)
print(fp1.get_failure_probabilities(0))
print(fp1.get_failure_probabilities(1))
print(fp1.get_failure_probabilities(5))
print(fp1.get_failure_probability()) """

""" print(e1.get_cost(0))
print(e1.get_failure_probability(0))
print(e1.get_cost(1))
print(e1.get_failure_probability(1))
print(player1.get_strategy_set()[1][0].get_id())
print(len(player1.get_strategy_set()))
print(player1.get_strategy_set() == player2.get_strategy_set()) """
#l1 = [1,2]
#l2 = [1,2]
#strategy_sets = [l1, l2]
""" listrep = list([1,2])
n = len(listrep)
l1_strategy_set = [("l1", [listrep[k] for k in range(n) if i&1<<k]) for i in range(2**n)]
l2_strategy_set = [("l2", [listrep[k] for k in range(n) if i&1<<k]) for i in range(2**n)]
p = list(itertools.product(*[l1_strategy_set, l2_strategy_set]))
for v in p:
    print(v)
print(len(p)) """

""" listrep = list([1,2,3,4])
player_id = "id"
n = len(listrep)
strategy_set = [[(player_id, listrep[k]) for k in range(n) if i&1<<k] for i in range(2**n)]
print(strategy_set)
print(len(strategy_set)) """