from typing import Dict

class Resource():

    def __init__(self, resource_id: int, cost: Dict[int, float], failure_probability: Dict[int, float]):
        """
        Constructor that gets run when main.py is invoked
        
        Parameters
        ----------
        resource_id : int
            resource's id

        cost : Dict[int, float]
            cost of this resource with congestion

        failure_probability : Dict[int, float]
            failure probability of this resource with congestion
        """

        self.__id = resource_id
        self.__costs: Dict[int, float] = cost
        self.__failure_probabilities = failure_probability

    def get_id(self) -> int:
        """
        Return resource's id

        Returns
        -------
        id : int
            resource's id
        """

        return self.__id

    def get_cost(self, congestion:int) -> float:
        """
        Return cost of resource given congestion
        
        Parameters
        ----------
        congestion : int
            congestion on this resource

        Returns
        -------
        costs : float
            cost
        """

        return self.__costs[congestion]

    def get_failure_probability(self, congestion:int) -> float:
        """
        Return failure probability given congestion
        
        Parameters
        ----------
        congestion : int
            congestion on this resource
        Returns
        -------
        failure_probabilities : float
            failure probability
        """

        return self.__failure_probabilities[congestion]

    def get_costs(self) -> Dict[int, float]:
        """
        Return costs of this resource

        Returns
        -------
        costs : Dict[int, float]
            costs
        """

        return self.__costs

    def get_failure_probabilities(self) -> Dict[int, float]:
        """
        Return failure probabilities of this resource

        Returns
        -------
        failure_probabilities : Dict[int, float]
            failure probabilities
        """

        return self.__failure_probabilities
    
    def set_id(self, resource_id: int):
        """
        Assign a new id to this resource
        
        Parameters
        ----------
        id : int
            resource's new id
        """

        self.__id = resource_id

    def set_cost(self, cost: float, congestion: int):
        """
        Assign a new cost to this resource at given congestion
        
        Parameters
        ----------
        cost : float
            resource's new cost
        
        congestion : int
            congestion 
        """

        self.__costs[congestion] = cost
    
    def set_failure_probability(self, failure_probability: float, congestion: int):
        """
        Assign a new failure probability to this resource at given congestion
        
        Parameters
        ----------
        failure_probability : float
            resource's new failure probability
        
        congestion : int
            congestion 
        """

        self.__failure_probabilities[congestion] = failure_probability