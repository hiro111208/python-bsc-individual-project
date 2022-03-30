import failure_probability
import cost

from typing import Dict

class Resource():

    def __init__(self, resource_id: int, cost: Dict[int, float], failure_probability: Dict[int, float]):
        self.id = resource_id
        self.costs = cost
        self.failure_probabilities = failure_probability

    def get_id(self) -> int:
        return self.id

    def get_cost(self, congestion:int) -> float:
        return self.costs[congestion]

    def get_failure_probability(self, congestion:int) -> float:
        return self.failure_probabilities[congestion]
    
    def set_id(self, resource_id:int): # id cant be changed in a simulation
        self.id = resource_id

    def set_cost(self, cost: Dict[int, float]):
        self.cost = cost
    
    def set_failure_probability(self, failure_probability: Dict[int, float]):
        self.failure_probability = failure_probability