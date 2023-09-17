"""
TUI for Checkers
"""

import time
from typing import Union, Dict

import click
from colorama import Fore, Style, Back
from checkers_exception import CheckersException, IncompleteMove
from logic import CheckersGame, PieceColor, PieceType, Piece, Player, CheckersMove
from checkers_move import CheckersMove
from bot import RandomBot, SmartBot

class TUIPlayer:
    """
    Simple class to store information about a TUI player
    A TUI player can either a human player using the keyboard,
    or a bot.
    """

    name: str
    bot: Union[None, RandomBot, SmartBot]
    game: CheckersGame
    color: PieceColor
    bot_delay: float

    def __init__(self, n: int, player_type: str, game: CheckersGame,
                color: PieceColor, opponent_color: PieceColor, bot_delay: float):
        """ Constructor
        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: The Connect-M board
            color: The player's color
            opponent_color: The opponent's color
            bot_delay: When playing as a bot, an artificial delay
             (in seconds) to wait before making a move.
        """

        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = RandomBot(game, color, opponent_color)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(game, color, opponent_color)
        self.game = game
        self.color = color
        self.bot_delay = bot_delay
        if self.color == PieceColor.BLACK:
            self.player = game._player1
        else:
            self.player = game._player2

    def get_move(self) -> int:
        """ Gets a move from the player
        If the player is a human player, prompt the player for a column.
        If the player is a bot, ask the bot to suggest a move.
        Returns: None
        """
        if self.bot is not None:
            time.sleep(self.bot_delay)
            suggestion = self.bot.suggest_move()
            return suggestion
        else:
            # Ask for a column (and re-ask if
            # a valid column is not provided)
            while True:
                print("\n" + "Please Choose a Piece" + "\n" + 
                "type row followed by space then column ex: 1 2")
                old = input(f"{self.player} old> ")
                old = (int(old.split()[0]) , int(old.split()[1]))
                
                piece = self.game._get_piece(old)
                if not piece:
                    print("Piece not found")
                    continue
                
                if not self.game._does_belong_to(piece._pos, self.player):
                    print("This piece is not yours. Please choose a different one")
                    continue
                try:
                    player_valid_moves = [i for i in 
                    self.game._player_valid_moves(self.player)[piece] if 
                        self.game._is_move_legal(i.from_pos , i.to_pos)]
                    print(f"legal moves are {player_valid_moves}")
                except CheckersException as e:
                    print(e)
                    continue
                if piece:
                    if self.game._does_belong_to(old , self.player):
                        #print(self.game._piece_valid_moves(old))
                        print("\n" + "Choose move from above" + "\n" + 
                        "type row followed by space then column ex: 1 2")
                        new = input(f"{self.player}  new> ")
                        new =(int(new.split()[0]) , int(new.split()[1]))
                        if self.game._is_move_legal(old , new):
                            return CheckersMove(old, new, piece)
                    else:
                        print("You chose a position that doesn't house a piece")
                        print("Please Choose a Piece" + "\n" + 
                        "type row followed by space then column ex: 1 2")
                        old = input(f"{self.player}  old> ")
                        old = (int(old.split()[0]) , int(old.split()[1]))


class TUI:

    """
    The GUI and TUI must provide a graphical and text-based interface, 
    respectively, capable of doing the following:

    Displaying a checkers board in its initial state 
    (with all the black and red pieces in their initial state)

    Provide a means to select a piece, and highlight 
    all possible moves for that piece.

    Provide a means to move a piece to a valid location.

    Display king pieces differently from regular pieces

    While the underlying game logic must support boards of arbitrary sizes, 
    you can assume that we will only test your TUI/GUI with boards from sizes 
    6x6 to 20x20 (i.e. 
    through 
    as defined in the “Generalization to Other Board Sizes” 
    section of the Design Requirements)

    While the underlying game logic must support resignations and draws, 
    you are not required to provide a user interface for this 
    (but may do so if you wish)
    make board dim public
    change class name to board
    """
    def print_board(board: CheckersGame):
        """
        Parameters: board (Checkers Game)
        takes in the current state of the game and prints a board, it prints the
        black side of the board next to the terminal to make it easier for the
        black player to choose pieces
        """
        #BLACKFIRST
        nrows = board._nrows
        ncols = board._nrows

        print(Fore.BLUE + "  ┌" + ("─┬" * (ncols-1)) + "─┐")
        for r in range(nrows):
            if r < 10:
                crow = str(r) + " " + Fore.BLUE + "│"
                num = r
            else:
                crow = str(r) + Fore.BLUE + "│"
                num = r
            for c in range(ncols):
                piece = board._get_piece((r, c))
                if piece is None:
                    crow +=   " " 
                elif piece._color == PieceColor.RED:
                    if piece._piece_type.value == PieceType.PAWN.value:
                        crow += Fore.RESET + Back.RED + Style.BRIGHT + "●" + Back.RESET
                    else:
                        #RED KING WILL BE GREEN
                        crow += Fore.RESET + Back.GREEN + Style.BRIGHT + "●" + Back.RESET
                elif piece._color == PieceColor.BLACK:
                    if piece._piece_type.value == PieceType.PAWN.value:
                        crow += Fore.RESET + Back.BLACK + Style.BRIGHT + "●" + Back.RESET
                    else:
                        #BLACK KING WILL BE YELLOW
                        crow += Fore.RESET + Back.YELLOW + Style.BRIGHT + "●" + Back.RESET
                crow += Fore.BLUE + Style.NORMAL + "│" + Fore.RESET
            print(Fore.RESET + crow)
            if r < nrows - 1:
                print(Fore.BLUE + "  ├" + ("─┼" * (ncols-1)) + "─┤")
            else:
                print(Fore.BLUE + "  └" + ("─┴" * (ncols-1)) + "─┘" + 
                Style.RESET_ALL)
        end = "  "
        for r in range(nrows):
            end += Fore.RESET + " " + str(r)[-1]
        print(end)

    def print_board_other_turn(board: CheckersGame):
        """
        Parameters: board (Checkers Game)
        takes in the current state of the game and prints a board, it prints the
        red side of the board next to the terminal to make it easier for the
        red player to choose pieces
        """
        #RED_FIRST  
        nrows = board._nrows
        ncols = board._nrows

        print(Fore.BLUE + "  ┌" + ("─┬" * (ncols-1)) + "─┐")
        for r in range(nrows - 1, -1, -1):
            if r < 10:
                crow = str(r) + " " + Fore.BLUE + "│"
                num = r
            else:
                crow = str(r) + Fore.BLUE + "│"
                num = r
            for c in range(ncols):
                piece = board._get_piece((r, c))
                if piece is None:
                    crow +=   " " 
                elif piece._color == PieceColor.RED:
                    if piece._piece_type.value == PieceType.PAWN.value:
                        crow += Fore.RESET + Back.RED + Style.BRIGHT + "●" + Back.RESET
                    else:
                        #RED KING WILL BE GREEN
                        crow += Fore.RESET + Back.GREEN + Style.BRIGHT + "●" + Back.RESET
                elif piece._color == PieceColor.BLACK:
                    if piece._piece_type.value == PieceType.PAWN.value:
                        crow += Fore.RESET + Back.BLACK + Style.BRIGHT + "●" + Back.RESET
                    else:
                        #BLACK KING WILL BE YELLOW
                        crow += Fore.RESET + Back.YELLOW + Style.BRIGHT + "●" + Back.RESET
                crow += Fore.BLUE + Style.NORMAL + "│" + Fore.RESET
            print(Fore.RESET + crow)
            if r != 0:
                print(Fore.BLUE + "  ├" + ("─┼" * (ncols-1)) + "─┤")
            else:
                print(Fore.BLUE + "  └" + ("─┴" * (ncols-1)) + "─┘" + Style.RESET_ALL)
        end = "  "
        for r in range(nrows):

            end += Fore.RESET + " " + str(r)[-1]
        print(end)
        return

def selection_handler(self):
    """
    function responsible for the selection handler that gives the player the 
    capability to choose game options
    """
    print("Please choose color")
    color = input()
    while (color != "BLACK") and (color != "RED"):
        print("Invalid input, choose again")
        color = input()
    print("Please choose opponent player type")
    player_type = input()
    while (player_type != "BOT") and (player_type != "HUMAN"):
        print("Invalid choice, please choose again")
        player_type = input()
    self.player = Player(color)
    self._opponent = Player("RED" if color == "BLACK" else "BLACK")
    tup = (color, player_type)
    return tup    

def play_checkers(game: CheckersGame, players: Dict[PieceColor, TUIPlayer]) -> None:
    """ Plays a game of Checkers on the terminal
    Args:
        game: the current state of the game
        players: A dictionary mapping piece colors to
          TUIPlayer objects.
    Returns: None
    """
    # The starting player is Black
    current = players[PieceColor.BLACK]

    # Keep playing until there is a winner:
    while not game._is_over:
        # Print the board
        if game._turn == game._player2:
            print()
            TUI.print_board(game)
            print()
        if game._turn == game._player1:
            print()
            TUI.print_board_other_turn(game)
            print()

        current_move = current.get_move()
        if current.bot is not None:
            game._move_checkers(current_move)
        else:
            try:
                game._move_piece(current_move.from_pos, current_move.to_pos)
            except IncompleteMove as e:
                game._move_no_exceptions(current_move.from_pos, current_move.to_pos)
                print(game)
                print("Please complete the move")
                continue
            while game._turn._color == current.color:
                time.sleep(1)
                print("still this persons", current.color)
                current_move = current.get_move()
                try:
                    game._move_piece(current_move.from_pos, current_move.to_pos)
                except IncompleteMove as e:
                    game._move_no_exceptions(current_move.from_pos, current_move.to_pos)
                    print(game)
                    print("Please complete the move")
                    continue
                except CheckersException as e:
                    print(e)
                    continue

        # Update the player
        if current.color == PieceColor.BLACK:
            current = players[PieceColor.RED]
        elif current.color == PieceColor.RED:
            current = players[PieceColor.BLACK]

    print()
    TUI.print_board(game)
    print()

    winner = game._get_winner()
    if winner is not None:
        print(f"The winner is {winner}!")
    else:
        print("It's a tie!")


def run_game( player1, player2, n, bot_delay=0.5):
    print(player1, player2)
    game = CheckersGame(n)

    player1 = TUIPlayer(1, player1, game, PieceColor.BLACK, PieceColor.RED, bot_delay)
    player2 = TUIPlayer(2, player2, game, PieceColor.RED, PieceColor.BLACK, bot_delay)

    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    play_checkers(game, players)


if __name__ == "__main__":
    print("Welcome to Checkers")
    print("You can quit the game at any point by entering CTRL+D")
    print("Please choose board game size")
    try:
        n = input()  
        n = int(n)
    except ValueError:
        print("Invalid, input board size must be integer")
        n = input()
        n = int(n)
    print("Please choose color, You can only choose RED or BLACK (Uppercase!)")
    color = input()
    while (color != "BLACK") and (color != "RED"):
        print("Invalid input, choose again")
        color = input()
    print("Please choose opponent player type")
    print("You can choose to be play against (HUMAN  RANDOM-BOT SMART-BOT) Uppercase!")
    player_type = input()
    while (player_type != "RANDOM-BOT") and (player_type != "HUMAN") and (player_type != "SMART-BOT"):
        print("Invalid choice, please choose again")
        player_type = input()

    if color == "BLACK":
        if player_type == "RANDOM-BOT":
            run_game( 'human', 'random-bot',int(n))
        if player_type == "HUMAN":
            run_game( 'human', 'human',int(n))
        if player_type == "SMART-BOT":
            run_game( 'human', 'smart-bot',int(n))
    if color == "RED":
        if player_type == "RANDOM-BOT":
            run_game('random-bot', 'human',int(n))
        if player_type == "HUMAN":
            run_game('human', 'human',int(n))
        if player_type == "SMART-BOT":
            run_game( 'smart-bot', 'human',int(n))
    # cmd()
