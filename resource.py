import failure_probability
import cost

class Resource():

    def __init__(self, name):
        self.name = name
        self.costs = cost.Cost() # cost would be a dict() in which a key is congestion (natural integers) and a value is cost due to the congestion
        #self.failure_probability = failure_probability # failure_probability would be a dict() in which a key is congestion (natural integers) and a value is failure_probability due to the congestion
        self.failure_probabilities = failure_probability.FailureProbability()
        costs = [5,15,6]
        for i in range(len(costs)):
            self.costs.update_costs(i, costs[i])
        probabilities = [0.5,0.2,0.3]
        for i in range(len(probabilities)):
            self.failure_probabilities.update_failure_probabilities(i, probabilities[i])

    def get_name(self):
        return self.name

    def get_cost(self, congestion):
        return self.costs.get_cost(congestion)

    def get_failure_probability(self, congestion):
        return self.failure_probabilities.get_failure_probability(congestion)
    def set_name(self, name):
        self.name = name

    """ def set_cost(self, cost):
        self.cost = cost """
    
    """ def set_failure_probability(self, failure_probabilities):
        self.failure_probability = failure_probabilities """