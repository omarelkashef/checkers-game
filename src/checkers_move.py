from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
PieceType = Enum("PieceType", ["PAWN", "KING"])

class CheckersMove:
    """
    Class to represent a checkers move of a certain piece
    """
    def __init__(self , from_pos , to_pos , piece , subsequent = None):
        """
        Constructor
        Parameters:
          from_pos(Tuple[int , int])): starting position of a move
          to_pos(Tuple[int , int]): end position of a move
          piece(Piece)
          subsequent(Optional[CheckersMove]): subsequent moves of that move
        """
        self.from_pos = from_pos
        self.to_pos = to_pos
        if not subsequent:
            self.subsequent = None
        else:
            self.subsequent = subsequent
        self.piece = piece
        self.jump = self.is_jump()
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        """
        returns a string representation of the move
        """
        curr = self
        to_str = f"{self.from_pos} --> {self.to_pos}"
        while curr.subsequent:
            curr = curr.subsequent
            to_str += f" --> {curr.to_pos}"
        return to_str
    
    def __eq__(self , other):
        """
        Checks equality of two moves if they have same start and end position
        as well same subsequent moves
        Parameters: other(CheckersMove)
        Returns: bool
        """
        if not isinstance(other , CheckersMove):
            return False
        return (self.from_pos == other.from_pos and self.to_pos == other.to_pos
               and self.subsequent == other.subsequent)
    
    def is_jump(self):
        """
        Checks whether a move is a jump or not
        Parameters: None
        Returns: bool
        """
        return (not abs(self.from_pos[0] - self.to_pos[0]) == 1
        and not abs(self.from_pos[1] - self.to_pos[1]) == 1)
    
    def does_include(self , other):
        if other.subsequent is None:
            return (self.from_pos == other.from_pos
               and self.to_pos == other.to_pos)
        return (self.from_pos == other.from_pos and self.to_pos == other.to_pos
            and self.subsequent.does_include(other))

    def to_list(self):
        """
        Returns a list representation of the move
        Parameters: None
        Returns: List[Tuple(int , int)]: coordinates covered by the move in 
        order
        """
        curr = self
        lst = [self.from_pos , self.to_pos]
        while curr.subsequent:
            curr = curr.subsequent
            lst += [curr.to_pos]
        return lst
    
    def does_it_king(self):
        """
        Checks whether a move results in kinging
        Parameters: None
        Returns: bool
        """
        return (self.piece._piece_type.value == PieceType.PAWN.value
           and self.get_end_position()[0] == self.piece.get_furthest_row())

    def get_jumped(self):
        """
        Returns the jumped position of the first move of a CheckersMove
        Parameters: None
        Returns: Tuple[int , int]
        """
        if not self.is_jump:
            return 
        row = (self.from_pos[0] + self.to_pos[0]) / 2
        col = (self.from_pos[1] + self.to_pos[1]) / 2
        return (int(row) , int(col))

    def has_same_start(self , other):
        """
        Checks if two move have the same starting steps 
        i.e. (3,3) --> (4,4) --> (5,5) has the same starting step as 
        (3,3) --> (4,4) --> (6,6) but not as (3,3) --> (1,1) --> (5,5)
        Parameters: other(CheckersMove)
        Returns: bool
        """
        assert isinstance(other , CheckersMove)
        return (self.from_pos == other.from_pos
            and self.to_pos == other.to_pos)
    
    def steps_num(self):
        """
        Returns number of steps in a move
        Parameters: None
        Returns: int
        """
        curr = self
        count = 1
        while curr.subsequent:
            curr = curr.subsequent
            count += 1
        return count
    
    def add_step(self , move):
        """
        Adds a step to of a move
        Parameters: position(Tuple[int , int])
        Returns: CheckersMove
        """
        assert isinstance(move , CheckersMove)
        if self.get_end_position() != move.from_pos:
            raise Exception(("from-position of the new step does not match" + 
                            " to-position of the last step"))
        curr = self
        tail = CheckersMove(curr.from_pos , curr.to_pos , curr.piece)
        dummy = CheckersMove(curr.from_pos , curr.to_pos , curr.piece)
        dummy.subsequent = tail
        while curr.subsequent:
            curr = curr.subsequent
            tail.subsequent = CheckersMove(curr.from_pos , curr.to_pos,
                                           curr.piece)
            tail = tail.subsequent
        tail.subsequent = move
        return dummy.subsequent
    
    def remove_last_step(self):
        """
        Removes the last step of a move. If the move is only one step, nothing 
        happens
        Parameters: None
        Returns: CheckersMove
        """
        curr = self
        for i in range(self.steps_num() - 2):
            curr = curr.subsequent
        curr.subsequent = None
        return self
    
    def get_end_position(self):
        """
        Returns end position of a move
        Parameters: None
        Returns: Tuple[int , int]
        """
        curr = self
        while curr.subsequent:
            curr = curr.subsequent
        return curr.to_pos
