class Player():

    def __init__(self, player_id: int, benefit: float):
        self.id = player_id # primary key int
        self.benefit = benefit

    def get_id(self) -> int:
        return self.id

    def get_benefit(self) -> float:
        return self.benefit

    def set_id(self, id):
        self.id = id

    def set_benefit(self, benefit):
        self.benefit = benefit