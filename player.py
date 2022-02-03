class Player():

    def __init__(self, player_id, benefit):
        self.id = player_id
        self.strategy_set = None
        self.benefit = benefit

    def get_benefit(self):
        return self.benefit

    # https://www.delftstack.com/ja/howto/python/powerset-python/
    def set_strategy_set(self, resources):
        listrep = list(resources)
        n = len(listrep)
        self.strategy_set = [(self, [listrep[k] for k in range(n) if i&1<<k]) for i in range(2**n)]

    def get_strategy_set(self):
        try:
            return self.strategy_set
        except:
            print("Strategy set has not been defined.")

    def get_id(self):
        return self.id