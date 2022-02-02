class Player():

    def __init__(self, name):
        self.name = name
        self.strategy_set = None

    # https://www.delftstack.com/ja/howto/python/powerset-python/
    def aquire_strategy_set(self, resources):
        listrep = list(resources)
        n = len(listrep)
        self.strategy_set = [[listrep[k] for k in range(n) if i&1<<k] for i in range(2**n)]

    def get_strategy_set(self):
        return self.strategy_set