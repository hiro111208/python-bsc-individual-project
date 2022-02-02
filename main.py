import resource
import player
import failure_probability

resource1 = resource.Resource("juice", 1, 0.5)
resource2 = resource.Resource("food", 2, 0.1)
resource3 = resource.Resource("game", 5, 0.8)
fp1 = failure_probability.FailureProbability()

player1 = player.Player("Hiro")
player1.aquire_strategy_set([resource1, resource2, resource3])
fp1.update_failure_probabilities(0, 5)

""" print(resource1.get_cost())
print(resource1.get_failure_probability())
print(player1.get_strategy_set())
print(len(player1.get_strategy_set())) """
print(fp1.get_failure_probabilities(0))