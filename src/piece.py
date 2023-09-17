from checkers_move import CheckersMove
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
PieceType = Enum("PieceType", ["PAWN", "KING"])
import copy

class Piece:
    """
    Class for representing a piece
    """

    def __init__(self, board, piece_color: PieceColor, position):
        """
        Constructor
        Parameters:
          board (CheckersBoard): Board on which piece is placed
          piece_color (str): color of the piece: either red or black
          position (tuple): tuple representing (row, column)
          idnum (string): id for each piece
        """
        # PieceColor, PieceType: Assignment of piece colors and pawn by default
        self._color = piece_color
        self._piece_type = PieceType.PAWN

        # Tuple[int , int]: position of piece
        self._pos = position

        # board attribute so that piece can access board
        self._board = board
    
    def __str__(self):
        """
        returns a string representation of the piece
        """
        if self._color.value == PieceColor.BLACK.value:
            if self._piece_type.value == PieceType.PAWN.value:
                return "b"
            else:
                return "B"
       #elif self._color == PieceColor.RED:
        else:
            if self._piece_type.value == PieceType.PAWN.value:
                return "r"
            else:
                return "R"
    
    def __repr__(self):
        if self._color.value == PieceColor.BLACK.value:
            color = "Black"
        else:
            color = "Red"
        if self._piece_type.value == PieceType.PAWN.value:
            piece_type = "Pawn"
        else:
            piece_type = "King"
        return f"({color},{piece_type},({self._pos[0]},{self._pos[1]})"
    
    #
    # PUBLIC METHODS
    #

    def update_pos(self , new_position):
        """
        Updates the coordinates of a piece to new row and new_column
        Parameters:
            new_position (tuple): new position represented as (row, column)
        Returns: None
       """
        assert self._board.is_valid_pos(new_position)
        self._pos = new_position
        return
            
    def virtual_move(self , new_position):
        """
        Virtually move a piece to a new position and creates a virtual updated 
        board without affecting the actual board
        Parameters: new_position(Tuple[row , col])
        Returns: virtual_piece(Piece): new virtual piece
        """
        virtual_piece = copy.deepcopy(self)
        virtual_piece._board = virtual_piece._board.create_virtual_board(
            virtual_piece._pos , new_position)
        virtual_piece._pos = new_position
        return virtual_piece

    def promote(self):
        """
        Promotes a piece to a king
        Parameters: None
        Returns: None
        """
        self._piece_type = PieceType.KING
        return
    
    def get_furthest_row(self):
        """
        Returns the furthest row from a player
        Parameters: None
        Returns: None
        """
        if self._color.value == PieceColor.RED.value:
            return 0
        else:
            return self._board._nrows - 1
    


