class Player():

    def __init__(self, player_id, benefit):
        self.id = player_id # primary key int
        #self.strategy_set = None
        self.benefit = benefit
        self.strategy = set()

    """ def get_strategy_set(self):
        try:
            return self.strategy_set
        except:
            print("Strategy set has not been defined.") """

    def get_id(self):
        return self.id

    def get_benefit(self):
        return self.benefit

    def get_strategy(self):
        return self.strategy

    def set_strategy(self, strategy: set):
        self.strategy = strategy