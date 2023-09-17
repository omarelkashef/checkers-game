from checkers_move import CheckersMove
import copy

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
        Returns a string representation of the board. Supports boards of size 
        up to 99 x 99
        """
        top_row = "  | " + "| ".join(str(i) +" " if i < 10 
                else str(i) for i in range(self._ncols)) +  "|"+ "\n"
        separator = "--+-" + "--+-" * self._ncols #+ "--|"
        board_str = top_row + separator + "\n"
        for i , j in enumerate(self._grid):
            row = str(i) + " | " if i < 10 else str(i) + "| "
            row += " | ".join([str(a) if a else "." for a in j]) + ' |'
            board_str += row + "\n" + separator + "\n"
        return "\n" + board_str
    
    def __repr__(self):
        return str(self)

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
        for piece , (row , col) in additions.items():
            if not self.is_valid_pos((row , col)):
                raise Exception("Invalid position")
            self._grid[row][col] = piece
        return 
    
    def remove_piece(self , position):
        """
        removes piece from the board
        Parameters:
            position(Tuple[int , int]): (row , column)
        Returns: piece(Piece)
        Raises: 
            Exception if row , col are not int or (row , col) is out of bound
        """
        if not self.is_valid_pos(position):
            raise Exception("Invalid position")
        row , col = position
        piece = self.get_piece(position)
        self._grid[row][col] = None
        return piece

    def reset(self):
        """ 
        Resets the board (removes all pieces and players)
        Parameters: None
        Returns: None
        """
        for row in self._grid:
            for i, _ in enumerate(row):
                row[i] = None
        return
    
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
        if (not self.is_valid_pos(old_position)
         or not self.is_valid_pos(new_position)):
            raise Exception("Invalid location")
        virtual_board = copy.deepcopy(self)
        virtual_board.update_piece_pos(old_position , new_position)
        return virtual_board
    
    def is_valid_pos(self , position):
        """
        Checks if a given position is valid(within bounds) or not
        """
        row , col = position
        return (isinstance(row , int) and isinstance(col , int) 
           and row < self._nrows and col < self._ncols
           and row >= 0 and col >= 0)

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
        if (not self.is_valid_pos(old_position)
         or not self.is_valid_pos(new_position)):
            raise Exception("Invalid position")
        piece = self.get_piece(old_position)
        old_row , old_col = old_position
        new_row , new_col = new_position
        self._grid[new_row][new_col] = piece
        self._grid[old_row][old_col] = None
        return 
    
    def get_piece(self , position):
        """
        Returns the piece a given position on the board
        Parameters:
          position(Tuple): (row,column)
        Returns: piece at position | False if poisiton is out of the board
        Raises: 
            Exception if row , column are not int
        """
        if position == ():  #position is out of bounds
            return False
        row , col = position
        if not isinstance(row , int) or not isinstance(col , int):
            raise Exception("Invalid position type")
        if row >= self._nrows or col >= self._nrows or row < 0 or col < 0:
            return False
        return self._grid[row][col]
    
    def coor_to_move(self , coordinates , piece):
        """
        Turns a list of coordinates into a CheckersMove object
        Parameters:
            coordinates(Tuple[int , int])
            piece(Piece)
        Returns: CheckersMove
        """
        assert len(coordinates) > 1
        move = CheckersMove(coordinates[0] , coordinates[1] , piece)
        i = 1
        curr = move
        while i <= len(coordinates) - 2:
            curr.subsequent = CheckersMove(coordinates[i] , coordinates[i + 1], 
                                        self)
            curr = curr.subsequent
            i += 1
        return move    
        