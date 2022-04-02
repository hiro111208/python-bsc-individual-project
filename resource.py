import failure_probability
import cost

from typing import Dict

class Resource():

    def __init__(self, resource_id: int, cost: Dict[int, float], failure_probability: Dict[int, float]):
        self.__id = resource_id
        self.__costs: Dict[int, float] = cost
        self.__failure_probabilities = failure_probability

    def get_id(self) -> int:
        return self.__id

    def get_cost(self, congestion:int) -> float:
        return self.__costs[congestion]

    def get_failure_probability(self, congestion:int) -> float:
        return self.__failure_probabilities[congestion]

    def get_costs(self) -> Dict[int, float]:
        return self.__costs

    def get_failure_probabilities(self) -> Dict[int, float]:
        return self.__failure_probabilities
    
    def set_id(self, resource_id: int):
        self.__id = resource_id

    def set_cost(self, cost: Dict[int, float], congestion: int):
        self.__costs[congestion] = cost
    
    def set_failure_probability(self, failure_probability: Dict[int, float], congestion: int):
        self.__failure_probabilities[congestion] = failure_probability