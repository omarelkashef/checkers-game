
from checkers_move import CheckersMove
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK","BORING"])

class Player:
    """
    Class for representing a player
    """
    def __init__(self , color: PieceColor):
        '''
        Constructor
        Args:
          color (str): color of the player: either red or black
        '''

        # PieceColor: Assignment of color
        self._color = color

        # set: Create empty set to store all of players' pieces
        self._pieces = set()
        
    def __str__(self):
        """
        returns a string representation of the player
        """
        return f"{self._color}"
    
    #
    # PUBLIC METHODS
    #

    def add_piece(self, piece):
        """
        Adds a piece to the player collection and adds it to the board
        Parameters: piece(Piece)
        Returns: None
        """
        self._pieces.add(piece)
        return

    def remove_piece(self, piece):
        """
        Removes a piece to the player collection
        Parameters: piece(Piece)
        Returns: None
        """
        self._pieces.remove(piece)
        return
    
    def reset(self):
        """
        Resets pieces of the player
        Parameters: None
        Returns: None
        """
        self._pieces = set()
        return 

class PlayerDraw(Player):
    """
    Class for representing a draw winner
    """
    def __init__(self):
        # PieceColor: Assignment of color
        super().__init__(PieceColor.BLACK) #BLACK is just a placeholder
        self._color = "DRAW"
    
    def __eq__(self , other):
        assert isinstance(other , Player)
        return self._color == other._color

