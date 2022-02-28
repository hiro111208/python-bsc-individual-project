class Cost():

    def __init__(self):
        self.costs = list() # should be dict of int key and float value

    def get_costs(self, key):
        try:
            return self.costs[key]
        except (TypeError, IndexError):
            print("No cost with the provided key.")

    def get_cost(self, key):
        try:
            return self.costs[key]
        except IndexError:
            print("No value with the key")

    def update_costs(self, key, value):
        try:
            if value < 0:
                print("Enter positive value")
            else:
                self.costs[key] = value
        except IndexError:
            self.costs.insert(key, value)
        except TypeError:
            print("Enter a valid number")