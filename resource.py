class Resource():

    def __init__(self, name, cost, failure_probability):
        self.name = name
        self.cost = cost # cost would be a dict() in which a key is congestion (natural integers) and a value is cost due to the congestion
        self.failure_probability = failure_probability # failure_probability would be a dict() in which a key is congestion (natural integers) and a value is failure_probability due to the congestion

    def get_name(self):
        return self.name

    def get_cost(self):
        return self.cost

    def get_failure_probability(self):
        return self.failure_probability

    def set_name(self, name):
        self.name = name

    def set_cost(self, cost):
        self.cost = cost

    def set_failure_probability(self, failure_probability):
        self.failure_probability = failure_probability