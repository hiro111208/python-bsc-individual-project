class FailureProbability():

    def __init__(self, failure_probabilities):
        #self.failure_probabilities = list() # should be dict of int key and float value
        self.failure_probabilities = failure_probabilities

    def get_failure_probability(self, key:int) -> float:
        try:
            return self.failure_probabilities[key]
        except (TypeError, IndexError):
            print("No probability with the provided key.")

    def update_failure_probabilities(self, key:int, value):
        try:
            if value >= 1 or value < 0:
                print("Enter value between 0 and 1")
            else:
                self.failure_probabilities[key] = value
        except IndexError:
            self.failure_probabilities.insert(key, value)
        except TypeError:
            print("Enter a valid number")