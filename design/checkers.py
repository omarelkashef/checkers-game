"""
Classes for implementing Checkers
Examples:
    1) Create a new Checkers game/board
      game = CheckersGame(n)
    2) Given a piece's position, check whether a given move is feasible
      is_possible_move = game._is_move_legal(old_position , new_position)
    3) Given a piece's position, obtain all valid moves for the piece
      piece_possible_moves = game._piece_valid_moves(position)
    4) Obtain dictionary that maps a piece to a list of all possible moves
    for a player
      player_possible_moves = game._player_possible_moves(player)
    5) Check whether there's a winner and determine the winner
      is_game_over = game._is_game_over()
      if is_game_over:
        print(game._get_winner())
      else:
"""
from enum import Enum
import copy
from player import Player
from board import Board
from piece import Piece
from checkers_move import CheckersMove
from checkers_exception import CheckersException , IncompleteMove

PieceColor = Enum("PieceColor", ["RED", "BLACK"])
PieceType = Enum("PieceType", ["PAWN", "KING"])

class CheckersGame:
    """
    Class for representing a checkersgame
    """

    def __init__(self, n):
        """
        Constructor
        Args:
          n (int): number of dark squares along a row
        """
        assert isinstance(n , int)
        # int: Integer family n
        self._n = n

        # int: Number of rows
        self._nrows = 2 * n + 2

        # player: Initialization of both players
        self._player1 = Player(PieceColor.BLACK)
        self._player2 = Player(PieceColor.RED)

        # list[list[Optional[Piece]]]: List representation of board
        self._state = Board(self._nrows , self._nrows , self._player1,
                            self._player2)

        #turn: Player
        self._turn = self._player1   #Black always starts first

        #is_over: bool
        self._is_over = False

        # Adding pieces to both players
        self._create_pieces(self._player1)
        self._create_pieces(self._player2)

    def __str__(self):
        """
        returns a string representation of the game
        """
        raise NotImplementedError


    def __repr__(self):
        raise NotImplementedError

    #
    # PRIVATE METHODS
    #

    def _create_pieces(self, player):
        """
        Creates all the pieces and adds them to their respective player
        collection
        Parameters:
          player: Player
        Returns: Nothing
        """
        raise NotImplementedError

    def _get_winner(self):
        """
        Returns the winner of the game or None if there is no winner
        Parameters: None
        Returns: Optional[Player]
        """
        raise NotImplementedError


    def _move_piece(self , old_position , new_position):
        """
        Moves a piece to a new location. If this move results in a win, game is
        ended. If not, turn is changed
        Parameters:
            old_position(Tuple[row , col])
            new_position(Tuple[row , col])
        Returns: None
        """
        raise NotImplementedError


    def _move_no_exceptions(self , old_position , new_position,
                            complete = False):
        """
        Moves a piece to a new location. It expectes a legal move and a valid
        position where a piece exists. It is a helper
        function for _move_piece() method that is called after the legality of
        the move is checked. It does not change turn or end game
        Parameters:
            old_position(Tuple[row , col])
            new_position(Tuple[row , col])
            complete(bool) passed in through helper
        Returns: None
        """
        raise NotImplementedError


    def _move_checkers(self , move):
        """
        Moves a piece to a new location. If this move results in a win, game is
        ended. If not, turn is changed. Better used for multi-step moves at
        once and bot moves. It should not be used with one step steps that are
        incomplete
        Parameters:
            move(CheckersMove)
        Returns: None
        """
        raise NotImplementedError

    def _check_after_turn(self):
        raise NotImplementedError


    def _remove_piece(self , position):
        """
        Removes a piece off the board and from player collection
        Parameters:
            position(Tuple[row , col])
        Returns:
            piece(Piece)
        """
        raise NotImplementedError

    def _end_game(self):
        """
        Ends the game and returns the winner player
        Parameters: None
        Returns: winner(Player)
        """
        raise NotImplementedError


    def _get_adjacent(self , position):
        """
        Returns adjacent cells that are legal to move to according to the
        piece type at a given position i.e. king can move diagonally forward and
        backwards but regular pieces can only move away from their starting
        position
        Parameters: position(Tuple[row , col])
        piece:
        Return: adjacent(List[Tuple[row,col]])
        """
        raise NotImplementedError


    def _get_legal_dir(self , position):
        """
        Returns adjacent directions that are legal to move to according to the
        piece type at a given position i.e. king can move diagonally forward and
        backwards but regular pieces can only move away from their starting
        position
        Parameters:
        virtual(Optional[Board]): not None only if it is a virtual move
        position(Tuple[row , col])
        Return: adjacent(List[Tuple[dir1,dir2]]): List of tuples of diagonal
        steps i.e. (1,1) means one diagonal step northeast
        """
        raise NotImplementedError


    def _get_pos_in_dir(self , position , direction , step):
        """
        Returns a new position that in a certain direction and certain steps
        away from a given position. Returns empty tuple if position is out of
        bounds
        Parameters:
            position(Tuple[row , col])
            direction(Tuple[row step , col step])
            step(int)
        Return: Tuple[row , col]
        """
        raise NotImplementedError


    def _create_virtual_state(self , old_position , new_position):
        """
        Creates a virtual state by moving a certain piece to a new position
        Parameters:
        old_position(Tuple[row , col])
        new_position(Tuple[row , col])
        Returns: state(Board): new virtual board
        """
        raise NotImplementedError


    def _create_virtual_game(self , old_position , new_position):
        """
        Creates a virtual game by moving a certain piece to a new position
        Parameters:
        old_position(Tuple[row , col])
        new_position(Tuple[row , col])
        Returns:virtual_game(CheckersGame): new virtual board
        """
        raise NotImplementedError


    def _can_be_jumped_to(self , piece , position):
        """
        Checks whether a given piece can jump into a certain position
        Parameters:
          virtual(Optional[Board]): not None only if it is a virtual move
          piece(Piece)
          position(Tuple[int , int]): (row,column)
        Returns: bool
        """
        raise NotImplementedError


    def _can_be_jumped(self , piece , position , jumped = []):
        """
        Checks whether a given piece can jump over a certain position
        Parameters:
          piece(Piece)
          position(Tuple[int , int]): (row,column)
        Return: bool
        """
        raise NotImplementedError


    def _get_piece(self , position):
        """
        Returns the piece a given position on the board
        Parameters:
          position(Tuple): (row,column)
        Returns: Optional[Piece] | False if poisiton is out of the board
        """
        raise NotImplementedError

    def _is_game_over(self): #depends on whether winner has to play the last move check Ed #1497
        """
        Checks if game has ended.
        Parameters: None
        Returns: bool
        """
        raise NotImplementedError


    def _end_turn(self):
        """
        Changes turns of the game
        Parameters: None
        Returns: None
        """
        raise NotImplementedError


    def _does_belong_to(self , position , player):
        """
        Checks if the the piece at a given position belongs to a player
        Parameters:
        position(Tuplep[int , int]): current piece position
        player (Player)
        Returns: bool
        """
        raise NotImplementedError


    def _is_move_legal(self , position , coordinates):
        """
        Checks if the Piece can move to a new position
        Parameters:
        position(Tuplep[int , int]): current piece position
        coordinates(List[Tuple[int , int]]) | Tuple[int , int]): list of
        given coordinates for a sequence of moves or a tuple for a single move
        Returns: bool
        """
        raise NotImplementedError


    def _is_move_complete(self , move):
        """
        Checks if the a move is complete or not i.e. all jumps have been
        exhausted
        Parameters:
        move(CheckresMove)
        position(Tuple[int , int]): end position of the move to be checked
        Returns: bool
        """
        raise NotImplementedError


    def _piece_valid_moves(self , position):
        """
        Checks all the possible moves for a piece given its position while
        considering whether a jump mus be performed or not
        Parameters: position(Tuple[int , int]): row , colimn
        Returns:
            List[CheckersMove]: list of CheckerMoves
        """
        raise NotImplementedError


    def _piece_semi_valid_moves(self , position):
        """
        Checks all the possible moves for a piece given its position without
        considering whether a jump mus be performed or not
        Parameters: position(Tuple[int , int]): row , colimn
        Returns:
            List[CheckersMove]: list of CheckerMoves
        """
        raise NotImplementedError


    def _get_jumps(self , position , directions , jumped = []):
        """
        Given a diagonal direction, it returns all end positions that would
        reult from any combination of multiple of single jump moves starting
        with those directions from a certain position

        Parameters:
            position(Tuple[int , int])
            directions(List[Tuple[int , int]]): list of intial directions
            jumped(List[Tuple[int , int]]): list of alraedy jumped positions
        Return: List[CheckersMove]: list of CheckersMove
        """
        raise NotImplementedError


    def _player_valid_moves(self , player):
        """
        Returns all the possible moves for that player considering all pieces
        Parameters:
            player(Player)
        Returns:
            Dictionary[Piece: List[CheckersMove]]
        """
        raise NotImplementedError


class Board:
    """
    Class for representing a generic board
    """

    def __init__(self , nrows , ncols , player1 , player2):
        """
        Constructor
        Parameters:
            nrows(int): number of rows
            ncols(int): number of columns
            player1(Player): player 1
            player2(Player): player 2
        """
        #int: number of rows
        self._nrows = nrows
        #int: number of columns
        self._ncols = ncols
        #Player: player 1
        self._player1 = player1
        #Player: player 2
        self._player2 = player2
        #List[List[Optional[Piece]]]: List representation of board
        self._grid = [[None] * self._ncols for _ in range(self._nrows)]

    def __str__(self):
        """
        Returns a string representation of the board
        """
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    #
    # PUBLIC METHODS
    #

    def add_pieces(self , additions):
        """
        Adds pieces to the board
        Parameters:
            additions(List[Dict[Piece:(row , col)]): List of dictionaries where
            the keys are the pieces and the values are locations
        Returns: None
        Raises:
            Exception if row , col are not int or (row , col) is out of bound
        """
        raise NotImplementedError

    def remove_piece(self , position):
        """
        removes piece from the board
        Parameters:
            position(Tuple[int , int]): (row , column)
        Returns: piece(Piece)
        Raises:
            Exception if row , col are not int or (row , col) is out of bound
        """
        raise NotImplementedError


    def reset(self):
        """
        Resets the board (removes all pieces and players)
        Parameters: None
        Returns: None
        """
        raise NotImplementedError


    def create_virtual_board(self , old_position , new_position):
        """
        Creates a virtual board by moving a certain piece from a given position
        to a new position without affecting actual board but does not change
        postion attriibute of piece
        Parameters:
        old_position(Tuple[row , col])
        new_position(Tuple[row , col])
        Returns: board(Board): new virtual board
        """
        raise NotImplementedError


    def is_valid_pos(self , position):
        """
        Checks if a given position is valid(within bounds) or not
        """
        raise NotImplementedError


    def update_piece_pos(self , old_position , new_position):
        """
        Moves a piece to a new location but does not update piece location
        Parameters:
            old_position (tuple): old position represented as (row, column)
            new_position (tuple): new position represented as (row, column)
        Raises:
            Exception if row , column are not int or (row , column)
            is out of bound
       """
        raise NotImplementedError


    def get_piece(self , position):
        """
        Returns the piece a given position on the board
        Parameters:
          position(Tuple): (row,column)
        Returns: piece at position | False if poisiton is out of the board
        Raises:
            Exception if row , column are not int
        """
        raise NotImplementedError


    def coor_to_move(self , coordinates , piece):
        """
        Turns a list of coordinates into a CheckersMove object
        Parameters:
            coordinates(Tuple[int , int])
            piece(Piece)
        Returns: CheckersMove
        """
        raise NotImplementedError


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
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


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
        raise NotImplementedError


    def virtual_move(self , new_position):
        """
        Virtually move a piece to a new position and creates a virtual updated
        board without affecting the actual board
        Parameters: new_position(Tuple[row , col])
        Returns: virtual_piece(Piece): new virtual piece
        """
        raise NotImplementedError


    def promote(self):
        """
        Promotes a piece to a king
        Parameters: None
        Returns: None
        """
        raise NotImplementedError


    def get_furthest_row(self):
        """
        Returns the furthest row from a player
        Parameters: None
        Returns: None
        """
        raise NotImplementedError


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
        raise NotImplementedError

    #
    # PUBLIC METHODS
    #

    def add_piece(self, piece):
        """
        Adds a piece to the player collection and adds it to the board
        Parameters: piece(Piece)
        Returns: None
        """
        raise NotImplementedError


    def remove_piece(self, piece):
        """
        Removes a piece to the player collection
        Parameters: piece(Piece)
        Returns: None
        """
        raise NotImplementedError


    def resign(self):
        """
        Requests a resign
        Parameters: None
        Returns: None
        """
        raise NotImplementedError

    def reset(self):
        """
        Resets pieces of the player
        Parameters: None
        Returns: None
        """
        raise NotImplementedError
