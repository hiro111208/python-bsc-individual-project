class StrategyProfile():
    def __init__(self, strategies, players, resources):
        self.strategies = strategies # key: player id, value: a set of resources
        self.players = players
        self.resources = resources
        self.congestion = None # key: resource_id, value: int
        self.even = None
        self.utilities = dict() # key: player_id, value: float
        self.set_congestion()
        self.check_even()
        self.calculate_utilities()

    def check_even(self):
        congestions = set()
        for congestion in self.congestion.values():
            congestions.add(congestion)
        if len(congestions) == 1:
            self.even = congestions.pop()

    def get_utilities(self):
        return self.utilities

    def get_strategies(self):
        return self.strategies

    def get_utility(self, player_id):
        # exception handling
        return self.utilities[player_id]

    def get_congestion(self):
        return self.congestion

    def set_congestion(self): # strategy profile is dict of 
        congestion = {key: 0 for key in self.resources}
        for strategy in self.strategies.values():
            for resource in strategy:
                congestion[resource] += 1
        self.congestion = congestion

    """ def set_congestion(self):
        congestion = dict()
        for strategy in self.strategies.values():
            for resource in strategy:
                if resource not in congestion:
                    congestion[resource] = 1
                else:
                    congestion[resource] += 1
        self.congestion = congestion """

    def calculate_utilities(self):
        for player_id, strategy in self.strategies.items():
            probability_product = 1
            total_cost = 0
            for resource in strategy:
                failure_probability = resource.get_failure_probability(self.congestion[resource])
                cost = resource.get_cost(self.congestion[resource])
                probability_product *= failure_probability
                total_cost += cost
            utility = player_id.get_benefit()*(1-probability_product) - total_cost
            self.utilities[player_id] = utility