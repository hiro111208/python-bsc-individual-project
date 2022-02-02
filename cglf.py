class CGLF():

    def __init__(self, ):
        self.players
        self.resources
        self.utilities
        self.strategy_set = None

    def calculate_utility(self, benefit, failure_probabilities, costs):
        failure_probability = 1
        for probability in failure_probabilities:
            failure_probability *= probability

        resource_cost = 0
        for cost in costs:
            resource_cost += cost

        return (1 - failure_probability) * benefit - cost

    # https://www.delftstack.com/ja/howto/python/powerset-python/
    def define_strategy_set(self):
        listrep = list(self.resources)
        n = len(listrep)
        self.strategy_set = [[listrep[k] for k in range(n) if i&1<<k] for i in range(2**n)]