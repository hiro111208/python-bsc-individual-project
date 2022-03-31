""" from typing import Dict
class Cost():

    def __init__(self, costs:Dict[int, float]):
        #self.costs = list() # should be dict of int key and float value
        self.costs = costs

    def get_cost(self, key:int) -> float:
        try:
            return self.costs[key]
        except (TypeError, IndexError):
            print("No cost with the provided key.")

    def update_costs(self, key:int, value:float):
        try:
            if value < 0:
                print("Enter positive value")
            else:
                self.costs[key] = value
        except IndexError:
            self.costs.insert(key, value)
        except TypeError:
            print("Enter a valid number") """