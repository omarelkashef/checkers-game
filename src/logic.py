"""
Classes for implementing Checkers
Examples:
    1) Create a new Checkers game/board
      game = CheckersGame(n)
    2) Given a piece's position, check whether a given move is feasible
      is_possible_move = game._is_move_legal(position)
    3) Given a piece's position, obtain all valid moves for the piece
      piece_possible_moves = game._piece_valid_moves(position)
    4) Obtain list of all possible moves for a player
      player_possible_moves = game._player_possible_moves(player)
    5) Check whether there's a winner and determine the winner
      is_game_over = game._is_game_over()
      if is_game_over:
        print(game._winner)
      else:
"""

from player import Player , PlayerDraw
from board import Board
from piece import Piece
from checkers_move import CheckersMove
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
PieceType = Enum("PieceType", ["PAWN", "KING"])
import copy
from checkers_exception import CheckersException , IncompleteMove


class CheckersGame:
    """
    Class for representing a checkersgame
    """
    REQUESTS = ["RESIGN" , "DRAW"]
    
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

        #game_moves: List[CheckersMove]
        self._game_moves = []

        #winner: Player
        self._winner = self._get_winner()

        #pending_request: Optional[str]
        self._pending_requests = []


    def __str__(self):
        """
        returns a string representation of the game
        """
        return str(self._state)
     
    
    def __repr__(self):
        return self.__str__()

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
        color = player._color
        if color.value == PieceColor.BLACK.value: 
            start_row = 0
            end_row = self._n
            step = 1
        else: #Red always starts on our side
            start_row = self._nrows - 1
            end_row = self._nrows - 1 - self._n
            step = -1
        for i in range(start_row , end_row , step):
            for j in range(self._nrows):
                # Considering dark squares only
                if (i + j) % 2 == 0:
                    new_piece = Piece(self._state, color, (i , j))
                    player.add_piece(new_piece)
                    self._state.add_pieces({new_piece: (i , j)})

    def _get_winner(self):
        """
        Returns the winner of the game or None if there is no winner
        Parameters: None
        Returns: Optional[Player]
        """
        if self._check_for_draw():
            return PlayerDraw()
        if not self._is_over:
            return None
        for player_piece_moves in (
            self._player_valid_moves(self._player1).values()):
            if player_piece_moves != []:
                return self._player1
        for player_piece_moves in (
            self._player_valid_moves(self._player2).values()):
            if player_piece_moves != []:
                return self._player2
        return None
    
    def _move_piece(self , old_position , new_position):
        """
        Moves a piece to a new location. If this move results in a win, game is
        ended. If not, turn is changed
        Parameters: 
            old_position(Tuple[row , col]) 
            new_position(Tuple[row , col]) 
        Returns: None
        """
        piece = self._get_piece(old_position)
        if not piece:
            raise CheckersException("No piece at given position")
        try:
            if not self._is_move_legal(old_position , new_position):
                raise CheckersException("Invalid move")
        except CheckersException as e:
            raise e
        move = CheckersMove(piece._pos , new_position , piece)
        is_complete_move = self._is_move_complete(move)
        self._move_no_exceptions(old_position , new_position , is_complete_move)
        if is_complete_move:
            self._check_after_turn()
        return

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
        piece = self._get_piece(old_position)
        move = CheckersMove(piece._pos , new_position , piece)
        self._state.update_piece_pos(old_position , new_position)
        piece.update_pos(new_position)
        if move.is_jump():
            if self._turn == self._player1:
                self._player2.remove_piece(self._get_piece(move.get_jumped()))
            elif self._turn == self._player2:
                self._player1.remove_piece(self._get_piece(move.get_jumped()))
            self._state.remove_piece(move.get_jumped())
        if move.does_it_king():
            piece.promote()
        self._game_moves += [move]
        return 
    
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
        if move.piece != self._get_piece(move.from_pos):
            raise CheckersException("No piece at given position") 
        curr_move = move
        if self._is_move_complete(curr_move):
            while curr_move:
                if self._is_move_legal(curr_move.from_pos , curr_move.to_pos):
                    self._move_no_exceptions(curr_move.from_pos,
                                             curr_move.to_pos)
                    curr_move = curr_move.subsequent
            if move.does_it_king():
                move.piece.promote()
            self._check_after_turn()
            return
        raise CheckersException 
    
    def _check_after_turn(self):
        """
        Performs necessary checking after each turn: if game is over and changes 
        _is_game_over and _turn attributes accrodingly 
        Parameters: None
        Returns: None
        """
        self._process_requests()
        if self._is_game_over():
            self._end_game()
        elif self._check_for_draw():
            self._end_game(PlayerDraw())
        else:
            self._end_turn()
        return   
    
    def _check_for_draw(self):
        """
        Checks whether there is a draw because of a < 40 non jumps streak
        Parameters: None
        Returns: bool
        """
        if len(self._game_moves) >= 40:
            for move in self._game_moves[-40:]:
                if not move.is_jump():
                    return False
        return False

    def _remove_piece(self , position):
        """
        Removes a piece off the board and from player collection
        Parameters: 
            position(Tuple[row , col]) 
        Returns:
            piece(Piece)
        """
        piece = self._get_piece(position)
        if piece._color.value == PieceColor.BLACK.value:
            player = self._player1
        elif piece._color.value == PieceColor.RED.value:
            player = self._player2
        if not piece:
            raise CheckersException("No piece at given position")
        self._state.remove_piece(position)
        player.remove_piece(piece)
        return piece        
 
    def _new_game(self):
        """ 
        Starts a new game and resets players, board, turn, pieces, etc.
        Parameters: None
        Returns: None
        """
        self._state.reset()
        self._player1.reset()
        self._player2.reset()
        self._create_pieces(self._player1)
        self._create_pieces(self._player2)
        self._turn = self._player1
        self._winner = None
        self._is_over = False
        return   
    
    def _end_game(self , winner = None):
        """ 
        Ends the game and sets the winner if not given.
        Parameters: winner(Optional[Player])
        Returns: None
        """
        self._is_over = True
        if not winner:
            self._winner = self._get_winner()
        else:
            self._winner = winner
        return

    def _can_process_request(self , request):
        """ 
        Checks whether it is an allowed time for a player to request a draw or 
        resign. We define that both have the same rules
        Parameters: request(Tuple[Player , str]): the string specifies the 
        request and has to be a valid request: "resign"  or "draw"
        Returns: bool
        """
        ### they can request a draw or to resign if it is the end of their and 
        ## they havealready made a move
        player , _ = request 
        if self._turn != player:
            return False
        if self._game_moves:
            if self._game_moves[-1].piece._color.value == player._color.value:
                return True
            else:
                return False
        return True
    
    def _add_request(self , request):
        """ 
        Adds a draw or resignation a player and declares the other a winner.
        We set rules for when it is allowed to resign the same as requesting
        a draw.
        Parameters: request(Tuple[Player , str]): the string specifies the 
        request and has to be a valid request: "resign"  or "draw"
        Returns: None
        """
        player , specific_request = request
        if specific_request.upper() not in self.REQUESTS:
            raise CheckersException("Not a valid request")
        self._pending_requests += [(player,specific_request.upper())]
        return
    
    def _process_requests(self):
        """ 
        Process a request of resignation at the right time and declares other 
        player as a winner
        Parameters: player(Player)
        Returns: None
        """
        if self._pending_requests:
            for i , request in enumerate(self._pending_requests):
                if self._can_process_request(request):
                    if request[1] == "RESIGN":
                        self._end_game(self._get_other_player(request[0]))
                    elif request[1] == "DRAW":
                        self._end_game(PlayerDraw())
                    self._pending_requests.pop(i)
        return

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
        curr_row , curr_col = position
        lst = []
        for step_row , step_col in self._get_adjacent_dir(position):
            new_pos = curr_row + step_row , curr_col + step_col
            lst += self.get_piece(new_pos)
        return lst
    
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
        piece = self._get_piece(position)
        if not piece:
            return []
        if piece._piece_type.value == PieceType.KING.value:
            adjacent = [(1 , 1) , (1 , -1) , (-1 , 1) , (-1 , -1)]
        else:
            if piece._color.value == PieceColor.BLACK.value:
                adjacent = [(1 , 1) , (1 , -1)]
            else:
                adjacent = [(-1 , 1) , (-1 , -1)]
        return adjacent 
    
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
        new_pos = (position[0] + step * direction[0], 
                position[1] + step * direction[1])
        if (new_pos[0] >= self._nrows or new_pos[1] >= self._nrows
        or new_pos[0] < 0 or new_pos[1] < 0):
            return ()
        else:
            return new_pos

    def _create_virtual_state(self , old_position , new_position):
        """
        Creates a virtual state by moving a certain piece to a new position
        Parameters: 
        old_position(Tuple[row , col])
        new_position(Tuple[row , col])
        Returns: state(Board): new virtual board
        """
        virtual_state = self._state.create_virtual_board(old_position,
                                                         new_position)
        virtual_state.get_piece(new_position).update_pos(new_position)
        return virtual_state

    def _create_virtual_game(self , old_position , new_position):
        """
        Creates a virtual game by moving a certain piece to a new position
        Parameters: 
        old_position(Tuple[row , col])
        new_position(Tuple[row , col])
        Returns:virtual_game(CheckersGame): new virtual board
        """
        virtual_game = copy.deepcopy(self)
        virtual_game._state = self._create_virtual_state(old_position,
                                                        new_position)
        return virtual_game

    def _can_be_jumped_to(self , piece , position):
        """
        Checks whether a given piece can jump into a certain position
        Parameters:
          virtual(Optional[Board]): not None only if it is a virtual move
          piece(Piece)
          position(Tuple[int , int]): (row,column)
        Returns: bool
        """
        return (position and self._get_piece(position) != False
               and self._get_piece(position) is None)
            
    def _can_be_jumped(self , piece , position , jumped = []):
        """
        Checks whether a given piece can jump over a certain position
        Parameters:
          piece(Piece)
          position(Tuple[int , int]): (row,column)
        Return: bool
        """
        if position is None or not isinstance(self._get_piece(position), 
                                             Piece):
            return False
        else:
            return (position not in jumped 
            and self._get_piece(position)._color != piece._color)
    
    def _get_piece(self , position):
        """
        Returns the piece a given position on the board
        Parameters:
          position(Tuple): (row,column)
        Returns: Optional[Piece] | False if poisiton is out of the board
        """
        return self._state.get_piece(position)
        
    def _is_game_over(self):
        """
        Checks if game has ended.
        Parameters: None
        Returns: bool
        """
        player = self._turn 
        other = self._get_other_player(self._turn)
        for player_piece_moves in self._player_valid_moves(other).values():
            if player_piece_moves != []:
                return False
        return True
    
    def _end_turn(self):
        """
        Changes turns of the game
        Parameters: None
        Returns: None
        """
        if self._turn == self._player1:
            self._turn = self._player2
        elif self._turn == self._player2:
            self._turn = self._player1
        return
    
    def _does_belong_to(self , position , player):
        """
        Checks if the the piece at a given position belongs to a player
        Parameters:
        position(Tuplep[int , int]): current piece position
        player (Player)
        Returns: bool
        """
        return (self._get_piece(position)
               and self._get_piece(position) in player._pieces)  
    
    def _is_move_legal(self , position , coordinates):
        """
        Checks if the Piece can move to a new position
        Parameters:
        position(Tuplep[int , int]): current piece position
        coordinates(List[Tuple[int , int]]) | Tuple[int , int]): list of 
        given coordinates for a sequence of moves or a tuple for a single move
        Returns: bool
        """
        piece = self._get_piece(position)
        potential_move = CheckersMove(position , coordinates , piece)
        for player_piece , player_move_lst in (
            self._player_valid_moves(self._turn).items()):
            for move in player_move_lst:
                if move.jump and not potential_move.jump:
                    raise CheckersException("Jump must be done when avaliable")
        for player_piece , player_move_lst in (
            self._player_valid_moves(self._turn).items()):
            for move in player_move_lst:
                if (player_piece == piece and
                   move.has_same_start(potential_move)):
                    return True
        return False
    
    def _is_move_complete(self , move):
        """
        Checks if the a move is complete or not i.e. all jumps have been 
        exhausted
        Parameters:
        move(CheckresMove)
        position(Tuple[int , int]): end position of the move to be checked
        Returns: bool
        """
        curr_start = move.from_pos
        curr_end = move.get_end_position()
        for piece_move in self._piece_valid_moves(curr_start):
            if piece_move.get_end_position() == curr_end:
                return True
        raise IncompleteMove("Move not complete")
    
    def _piece_valid_moves(self , position):
        """
        Checks all the possible moves for a piece given its position while
        considering whether a jump mus be performed or not
        Parameters: position(Tuple[int , int]): row , colimn
        Returns:
            List[CheckersMove]: list of CheckerMoves
        """
        rv = {"jump": [] , "no_jump": [] }
        for move in self._piece_semi_valid_moves(position):
            if move.jump:
                rv["jump"] += [move]
            else:
                 rv["no_jump"] += [move]
        if rv["jump"]!= []:
            return rv["jump"]
        return rv["no_jump"]

    def _piece_semi_valid_moves(self , position):
        """
        Checks all the possible moves for a piece given its position without
        considering whether a jump mus be performed or not
        Parameters: position(Tuple[int , int]): row , colimn
        Returns:
            List[CheckersMove]: list of CheckerMoves
        """
        legal_moves  = []
        adjacent = self._get_legal_dir(position)
        for direction in adjacent:
            new_pos = self._get_pos_in_dir(position , direction , step = 1)
            piece_at_new_pos = self._get_piece(new_pos)
            if piece_at_new_pos == False:
                continue
            if piece_at_new_pos is None:
                legal_moves += ([CheckersMove(position , new_pos,
                self._get_piece(position))])
            else:
                legal_moves += self._get_jumps(position , [direction] ,[])
        return legal_moves

    def _get_jumps(self , position , directions , jumped = []):
        """
        Given a list of diagonal directions, it returns all end positions that
        would reult from any combination of multiple of single jump moves 
        starting with those directions from a certain position

        Parameters: 
            position(Tuple[int , int])
            directions(List[Tuple[int , int]]): list of intial directions
            jumped(List[Tuple[int , int]]): list of alraedy jumped positions
        Return: List[CheckersMove]: list of CheckersMove
        """
        curr_pos = position
        curr_piece = self._get_piece(curr_pos)
        lst = []
        for direction in directions:
            pos_to_jump_to = self._get_pos_in_dir(curr_pos , direction,
                                                       step = 2)
            pos_to_be_jumped = self._get_pos_in_dir(curr_pos , direction,
                                                          step = 1)
            if (not self._can_be_jumped(curr_piece , pos_to_be_jumped , jumped)
              or not self._can_be_jumped_to(curr_piece , pos_to_jump_to)):
                   continue
            virtual_piece = curr_piece.virtual_move(pos_to_jump_to)
            move = CheckersMove(curr_pos,pos_to_jump_to,curr_piece)
            if move.does_it_king():
                lst += [move]
                continue 
            virtual_state = self._create_virtual_state(curr_pos,pos_to_jump_to)
            tmp = self._state
            self._state = virtual_state
            subsequent_jumps = self._get_jumps(pos_to_jump_to,
                                            self._get_legal_dir(pos_to_jump_to), 
                                            jumped + [pos_to_be_jumped])
            if subsequent_jumps:                                
                for jump in subsequent_jumps:
                    lst += [move.add_step(jump)]
            else: 
                lst += [move]
            self._state = tmp
        return lst
    
    def _player_valid_moves(self , player):
        """
        Returns all the possible moves for that player considering all pieces
        Parameters: 
            player(Player)
        Returns:
            Dictionary[Piece: List[CheckersMove]]
        """
        rv = {}
        for piece in player._pieces:
            rv[piece] = self._piece_valid_moves(piece._pos)
        return rv
    
    def _get_other_player(self , player):
        """
        Returns the other player(who is not input)
        Parameters: player(Player)
        Returns: Player
        """
        if player == self._player1:
            return self._player2
        if player == self._player2:
            return self._player1    
