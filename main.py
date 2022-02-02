import resource
import player
import failure_probability

resource1 = resource.Resource("juice", 1, 0.5)
resource2 = resource.Resource("food", 2, 0.1)
resource3 = resource.Resource("game", 5, 0.8)
fp1 = failure_probability.FailureProbability()
fp2 = failure_probability.FailureProbability()


player1 = player.Player("Hiro")
player1.aquire_strategy_set([resource1, resource2, resource3])

""" fp1.update_failure_probabilities(0, 0.8)
print(fp1.get_failure_probabilities(0))
fp1.update_failure_probabilities("a", 0.5)
print(fp1.get_failure_probabilities(0))
print(fp1.get_failure_probabilities(1))
print(fp1.get_failure_probabilities(5))
print(fp1.get_failure_probability()) """

print(resource1.get_cost(1))
print(resource1.get_failure_probability(3))
#print(player1.get_strategy_set())
print(len(player1.get_strategy_set()))