class StrategyProfile():
    def __init__(self, players):
        self.players = players
        self.utilities = dict()

    def get_utilities(self):
        return self.utilities

    def get_players(self):
        return self.players