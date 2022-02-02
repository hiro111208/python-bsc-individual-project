class FailureProbability():

    def __init__(self):
        self.failure_probabilities = list()
        # self.set_failure_probabilities(failure_probabilities)

    def get_failure_probabilities(self, key):
        try:
            return self.failure_probabilities[key]
        except (TypeError, IndexError):
            print("No probability with the provided key.")

    def update_failure_probabilities(self, key, value):
        try:
            if value >= 1 or value < 0:
                print("Enter value between 0 and 1")
            else:
                self.failure_probabilities.insert(key, value)
            """ if not self.failure_probabilities:
                self.failure_probabilities.insert(key, value)
            if key > len(self.failure_probabilities):
                self.failure_probabilities[len(self.failure_probabilities) + 1] = value
            else:
                self.failure_probabilities[1] = value """
        except TypeError:
            print("Enter a valid number")
        #self.failure_probabilities = failure_probabilities.sort()