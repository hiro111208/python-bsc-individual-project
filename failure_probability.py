class FailureProbability():

    def __init__(self):
        self.failure_probabilities = list()

    def get_failure_probabilities(self, key):
        try:
            return self.failure_probabilities[key]
        except (TypeError, IndexError):
            print("No probability with the provided key.")

    def get_failure_probability(self, key):
        try:
            return self.failure_probabilities[key]
        except IndexError:
            print("No value with the key")

    def update_failure_probabilities(self, key, value):
        try:
            if value >= 1 or value < 0:
                print("Enter value between 0 and 1")
            else:
                self.failure_probabilities[key] = value
        except IndexError:
            self.failure_probabilities.insert(key, value)
        except TypeError:
            print("Enter a valid number")