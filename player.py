class Player():

    def __init__(self, player_id: int, benefit: float):
        self.__id = player_id # primary key int
        self.__benefit = benefit

    def get_id(self) -> int:
        return self.__id

    def get_benefit(self) -> float:
        return self.__benefit

    def set_id(self, id: int):
        self.__id = id

    def set_benefit(self, benefit: float):
        self.__benefit = benefit