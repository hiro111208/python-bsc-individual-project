class Cost():

    def __init__(self, costs):
        self.set_costs(costs)

    def get_costs(self):
        return self.costs

    def set_costs(self, costs):
        self.costs = costs.sort()