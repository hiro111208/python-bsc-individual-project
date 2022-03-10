class Cost():

    def __init__(self):
        #self.costs = list() # should be dict of int key and float value
        self.costs = {1:1, 2:1/4}

    def get_cost(self, key:int):
        try:
            return self.costs[key]
        except (TypeError, IndexError):
            print("No cost with the provided key.")

    def update_costs(self, key:int, value):
        try:
            if value < 0:
                print("Enter positive value")
            else:
                self.costs[key] = value
        except IndexError:
            self.costs.insert(key, value)
        except TypeError:
            print("Enter a valid number")