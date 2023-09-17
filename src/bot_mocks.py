"""
CheckersMock
This subclass inherits from CheckersGame and uses a different constructor
method, which does not create all the pieces for both players upon
initialization.

Instead, the CheckersMock subclass has another _man_add_piece method so that
different board states and testing situations can be used to evaluate
the bots' suggested moves.

"""

from logic import CheckersGame, PieceColor, Player, Board, Piece

class CheckersMock (CheckersGame):
    """
    Class for representing a mock checkersgame
    Constructor does not automatically fill starting pieces for both places
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

        #game_moves: List[CheckersMove]
        self._game_moves = []

        #winner: Player
        self._winner = self._get_winner()

        #pending_request: Optional[str]
        self._pending_requests = []


    #
    # PRIVATE METHODS
    #

    def _man_add_piece(self, color, pos):
        """
        Manually adds pieces to both sides for testing purposes

        Parameters:
            color: PieceColor
            pos: Tuple[row, col]

        Returns: (does not return a value)
        """
        if color == PieceColor.BLACK:
            player = self._player1
        elif color == PieceColor.RED:
            player = self._player2
        else:
            raise ValueError("Player color does not match black or red")

        new_piece = Piece(self._state, color, pos)
        player.add_piece(new_piece)
        self._state.add_pieces({new_piece: pos})
