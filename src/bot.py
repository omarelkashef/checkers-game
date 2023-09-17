"""
BOTS FOR CHECKERS
(and command for running simulations with bots)

Contains a parent Bot superclass and two child SmartBot and RandomBot classes

The smart bot carries out the following strategies in the order of priority:
        1. Carry out a winning move if it exists
        2. Promote a piece to king if possible
        3. Capture more rather than fewer pieces if the player must capture
        4. Avoid moving the back row pieces
        (only move the back row if no other move is possible)

Below are the online sources for the above strategies:

https://www.thesprucecrafts.com/how-to-win-at-checkers-411170
- Your Goal Should Be Getting a Checker to the End of the Board
- Trade Pieces When You Are Ahead
- Leave Your Home Row Checkers Until You Need Them

https://www.ultraboardgames.com/checkers/tips.php
6. Crown your pieces to kings
8. Trade pieces when you are ahead
9. Move your home row checkers only when you need them

"""
import random
from typing import Union, List
from abc import ABC, abstractmethod
import click

from logic import PieceColor, CheckersGame, Player, CheckersMove


#
# BOTS
#

class Bot(ABC):
    """
    Abstract parent class for RandomBot and SmartBot
    """

    _game: CheckersGame
    _color: PieceColor
    _opponent_color: PieceColor
    player: Player

    def __init__(self, game, color: PieceColor, opponent_color: PieceColor):
        """
        Constructor

        Args:
            game: Current game state of checkers which the bot will play on
            color: Bot's color
            opponent_color: Opponent's color
        """
        self._game = game
        self._color = color
        self._opponent_color = opponent_color

        if color == PieceColor.BLACK and opponent_color == PieceColor.RED:
            self.player = game._player1
        elif color == PieceColor.RED and opponent_color == PieceColor.BLACK:
            self.player = game._player2
        else:
            raise ValueError("Player color does not match black or red")

    @abstractmethod
    def suggest_move(self) -> CheckersMove:
        """
        Placeholder abstract method for Bot to suggest a move

        Parameters:
            none

        Returns: CheckersMove
        """
        raise NotImplementedError

    def _convert_move_dict(self, move_dict) -> List[CheckersMove]:
        """
        Converts move dictionary {Piece: lst[CheckersMove]} into
        lst[CheckersMove] which is more easily iterable

        Also selects only jumping moves out of move dictionary
        by filtering and checking if any move.is_jump
        i.e. bot must capture if it is possible to capture any opponent piece

        Parameters:
            move_dict: Dict{Piece: lst[CheckersMove]}

        Returns: lst[CheckersMove]
        """
        # Converts dictionary into list form
        all_moves = []
        for piece in move_dict:
            all_moves += move_dict[piece]

        must_jump = False
        jump_moves = []

        # Checks if a capture must be made and filters capture moves
        for move in all_moves:
            if move.is_jump():
                must_jump = True
                jump_moves.append(move)

        return jump_moves if must_jump else all_moves

class RandomBot(Bot):
    """
    Simple Bot that just picks a move at random
    """

    _game: CheckersGame
    _color: PieceColor
    _opponent_color: PieceColor
    player: Player

    def __init__(self, game, color: PieceColor, opponent_color: PieceColor):
        """
        Constructor

        Args:
            game: Current game state of checkers which the bot will play on
            color: Bot's color
            opponent_color: Opponent's color
        """
        super().__init__(game, color, opponent_color)

    def suggest_move(self) -> CheckersMove:
        """
        Suggests a random move
        Takes all possible moves and picks a random one

        Parameters: none

        Returns: (piece, move) tuple where a move is lst[Tuple[int]]

        """
        move_dict = self._game._player_valid_moves(self.player)
        all_moves = self._convert_move_dict(move_dict)

        return random.choice(all_moves)

class SmartBot(Bot):
    """
    The smart bot carries out the following strategies in the order of priority:
        1. Carry out a winning move if it exists
        2. Promote a piece to king if possible
        3. Capture more rather than fewer pieces if the player must capture
        4. Avoid moving the back row pieces
        (only move the back row if no other move is possible)
    """

    _game: CheckersGame
    _color: PieceColor
    _opponent_color: PieceColor
    player: Player

    def __init__(self, game, color: PieceColor, opponent_color: PieceColor):
        """
        Constructor

        Args:
            game: Current game state of checkers which the bot will play on
            color: Bot's color
            opponent_color: Opponent's color
        """
        super().__init__(game, color, opponent_color)

    def _backrow_move(self, move):
        """
        Helper function which checks if a move involves shifting a pawn
        from the back row of the board

        Parameters:
            move: CheckersMove

        Returns: bool
        """
        # First row is 0 for black player and 2n + 2 for red player
        first_row = {PieceColor.BLACK: 0, PieceColor.RED: self._game._nrows - 1}

        return move.from_pos[0] == first_row[self._color]

    def _longest_capture(self, move_list) -> List[CheckersMove]:
        """
        Takes a list of jumping moves and
        returns a list which contains the longest

        Paremeters:
            move_list: lst[CheckersMove]

        Returns: lst[CheckersMove]
        """
        max_step = 1
        longest_moves = []
        for move in move_list:
            # Find a new longest_move: update the max_step
            if move.steps_num() > max_step:
                longest_moves = [move]
                max_step = move.steps_num()

            # Add another longest_move
            if move.steps_num() == max_step and max_step > 1:
                longest_moves.append(move)

        return longest_moves

    def _move_wins(self, move) -> bool:
        """
        Checks if a move of a piece into a certain position results in a win
        Creates a temporary virtual state and assesses if a winner exists

        Parameters:
            move(CheckersMove)

        Returns: bool
        """
        tmp = self._game._state
        virtual_state = self._game._create_virtual_state(move.from_pos,
                                                   move.to_pos)
        self._game._state = virtual_state
        if move.steps_num() == 1:
            move_wins = self._game._get_winner() is not None
            self._game._state = tmp
            return move_wins

        # Recursive checking for multi-jump captures
        move_wins = self._move_wins(move.subsequent)
        self._game._state = tmp
        return move_wins

    def suggest_move(self):
        """
        Suggests a move

        First generates a priority_moves list based on the above strategy
        Takes the first element of priority_moves list as the suggested move

        Parameters: none

        Returns: CheckersMove

        """
        move_dict = self._game._player_valid_moves(self.player)
        all_moves = self._convert_move_dict(move_dict)

        long_list = self._longest_capture(all_moves) if all_moves[0].jump \
            else []

        winning_move = []
        king_move = []
        general_move = []
        backrow_move =[]

        for move in all_moves:
            if not move.jump and self._move_wins(move):
                winning_move.append(move)

            if move.does_it_king():
                king_move.append(move)

            elif self._backrow_move(move):
                # Avoid making moves which start from first row of board
                # Shift remaining backrow_moves to last priority
                backrow_move.append(move)

            elif move not in long_list:
                # The move does not match any special situation/condition
                general_move.append(move)

        # Randomly shuffle moves which belong to the same category
        for move_list in \
            [winning_move, king_move, long_list, general_move, backrow_move]:
            random.shuffle(move_list)

        # Concatenate all lists of moves together in desired priority
        priority_moves = winning_move + king_move + \
            long_list + general_move + backrow_move

        # Obtain the first priority in the priority_moves list
        return priority_moves[0]

#
# SIMULATION CODE
#
# This is not strictly required in the course project,
# but writing something like this may be useful to
# test your bot(s)
#

class BotPlayer:
    """
    Simple class to store information about a
    bot player in a simulation.
    """

    name: str
    bot: Union[RandomBot, SmartBot]
    color: PieceColor
    wins: int

    def __init__(self, name: str, game: CheckersGame, color: PieceColor,
                 opponent_color: PieceColor):
        """
        Constructor
        Args:
            name: Name of the bot (random or smart)
            game: State of the current CheckersGame
            color: Bot's color
            opponent_color: Opponent's color
        """
        self.name = name

        if self.name == "random":
            self.bot = RandomBot(game, color, opponent_color)
        elif self.name == "smart":
            self.bot = SmartBot(game, color, opponent_color)
        self.color = color
        self.wins = 0


def simulate(game: CheckersGame, n: int, bots):
    """ Simulates multiple games between two bots
    Args:
        board: The board to play on
        n: The number of matches to play
        bots: Dictionary mapping piece colors to
            BotPlayer objects (the bots what will
            face off in each match)
    Returns: None
    """
    for _ in range(n):
        game._new_game()
        game._is_over = False

        # The starting player is Black
        current_player = bots[PieceColor.BLACK]

        # While the game isn't over, make a move
        while not game._is_over:
            current_move = current_player.bot.suggest_move()
            print(game)
            print(current_move)
            game._move_checkers(current_move)

            # Update the player
            if current_player.color == PieceColor.BLACK:
                print("RED's turn")
                current_player = bots[PieceColor.RED]
            elif current_player.color == PieceColor.RED:
                print("BLACK's turn")
                current_player = bots[PieceColor.BLACK]

        # If there is a winner, add one to that
        # bot's tally
        winner = game._get_winner()
        print("The winner is", winner)
        if winner is not None:
            bots[winner._color].wins += 1

@click.command(name="checkers-bot")
@click.option('-n', '--num-games',  type=click.INT, default=100)
@click.option('--player1',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
@click.option('--player2',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
def cmd(num_games, player1, player2):
    """
    Simulation of 100 n=3 games from the command line
    Parameters:
        num_games: int
        player1: str
        player2: str

    Returns: (does not reu=turn a value)
    """
    game = CheckersGame(3)

    bot1 = BotPlayer(player1, game, PieceColor.BLACK, PieceColor.RED)
    bot2 = BotPlayer(player2, game, PieceColor.RED, PieceColor.BLACK)

    bots = {PieceColor.BLACK: bot1, PieceColor.RED: bot2}

    simulate(game, num_games, bots)

    bot1_wins = bots[PieceColor.BLACK].wins
    bot2_wins = bots[PieceColor.RED].wins
    ties = num_games - (bot1_wins + bot2_wins)

    print(f"Bot 1 ({player1}) wins: {100 * bot1_wins / num_games:.2f}%")
    print(f"Bot 2 ({player2}) wins: {100 * bot2_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")

if __name__ == "__main__":
    cmd()
