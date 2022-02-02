class Strategy():

    def __init__(self, resources):
        self.resources = resources

    def get_resources(self):
        return self.resources

    def set_resources(self, resources):
        self.resources = resources