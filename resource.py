import failure_probability
import cost

class Resource():

    def __init__(self, resource_id):
        self.id = resource_id # primary id
        self.costs = cost.Cost() # cost would be a dict() in which a key is congestion (natural integers) and a value is cost due to the congestion
        #self.failure_probability = failure_probability # failure_probability would be a dict() in which a key is congestion (natural integers) and a value is failure_probability due to the congestion
        self.failure_probabilities = failure_probability.FailureProbability()
        """ costs = [1, 1/4] # cost must be increasing
        for i in range(len(costs)):
            self.costs.update_costs(i, costs[i]) """
        """ probabilities = [0.01, 0.26]
        for i in range(len(probabilities)):
            self.failure_probabilities.update_failure_probabilities(i, probabilities[i]) """

    def get_id(self):
        return self.id

    def get_cost(self, congestion:int) -> float:
        return self.costs.get_cost(congestion)

    def get_failure_probability(self, congestion:int) -> float:
        return self.failure_probabilities.get_failure_probability(congestion)
    
    def set_id(self, resource_id): # id cant be changed in a simulation
        self.id = resource_id

    """ def set_cost(self, cost):
        self.cost = cost """
    
    """ def set_failure_probability(self, failure_probabilities):
        self.failure_probability = failure_probabilities """