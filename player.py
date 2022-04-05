class Player():

    # Consructor: this gets run when main.py is invoked
    def __init__(self, player_id: int, benefit: float):
        """
        Constructor that gets run when main.py is invoked
        
        Parameters
        ----------
        player_id : Dict[int, Player]
            player's id

        benefit : float
            player's benefit
        """

        self.__id = player_id # primary key int
        self.__benefit = benefit

    def get_id(self) -> int:
        """
        Return player's id

        Returns
        -------
        id : int
            player's id
        """

        return self.__id

    def get_benefit(self) -> float:
        """
        Return player's benefit

        Returns
        -------
        float : float
            player's benefit
        """

        return self.__benefit

    def set_id(self, id: int):
        """
        Assign a new id to this player
        
        Parameters
        ----------
        id : int
            player's new id
        """

        self.__id = id

    def set_benefit(self, benefit: float):
        """
        Assign a new benefit to this player
        
        Parameters
        ----------
        benefit : float
            player's new benefit
        """

        self.__benefit = benefit