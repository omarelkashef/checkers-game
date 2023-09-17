"""
TESTS FOR CHECKERS BOT

We want to test if the bot can carry out the following strategies
in this order of priority:
1. Carry out a winning move if it exists
2. Promote a piece to king if possible
3. Capture more rather than fewer pieces if the player must capture
4. Avoid moving the back row pieces
    (only move the back row if no other move is possible)
"""

from bot import RandomBot, SmartBot, BotPlayer, simulate
from logic import CheckersGame, PieceColor
from bot_mocks import CheckersMock

#
# RANDOM TESTS
#

def test_random_1():
    """
    Preliminary test to check if RandomBot returns
    legal move on new Checkers Board
    n = 2, PieceColor.BLACK
    """
    new_game = CheckersGame(2)

    randombot = RandomBot(new_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = randombot.suggest_move()

    assert new_game._is_move_legal(suggestion.from_pos, suggestion.to_pos)

def test_random_2():
    """
    Checks if RandomBot returns legal move for PieceColor.RED player
    after PieceColor.BLACK player has moved a piece
    (i.e. verifies RandomBot returns move in middle of game)
    n = 2, PieceColor.RED
    """
    new_game = CheckersGame(2)
    new_game._move_piece((1,1), (2,0))
    randombot = RandomBot(new_game, PieceColor.RED, PieceColor.BLACK)
    suggestion = randombot.suggest_move()

    assert new_game._is_move_legal(suggestion.from_pos, suggestion.to_pos)

def test_random_3():
    """
    Verifies that Randombot returns a valid / feasible move given Situation A

    Situation A Description
    We assume that all pieces are pawns and not kings.

    There are five black pieces "B0, B1, B2, B3, B4" and one red piece "R".
    [
        ["B4", None, None, None, None, None],
        [None, None, None, None, None, "B3"],
        ["B0", None, "B1", None, None, None],
        [None, None, None, None, None, None],
        ["R", None, None, None, "B2", None],
        [None, None, None, None, None, None]
    ]

    n = 2, PieceColor.BLACK
    """
    mock_game = CheckersMock(2)
    mock_game._man_add_piece(PieceColor.BLACK, (0,0))
    mock_game._man_add_piece(PieceColor.BLACK, (1,5))
    mock_game._man_add_piece(PieceColor.BLACK, (4,4))
    mock_game._man_add_piece(PieceColor.BLACK, (2,2))
    mock_game._man_add_piece(PieceColor.BLACK, (2,0))
    mock_game._man_add_piece(PieceColor.RED, (4,0))

    randombot = RandomBot(mock_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = randombot.suggest_move()

    assert mock_game._is_move_legal(suggestion.from_pos, suggestion.to_pos)

def test_random_4():
    """
    Checks that Randombot returns only move if there is only one move left
    given Situation A

    n = 2, PieceColor.RED
    """
    mock_game = CheckersMock(2)
    mock_game._man_add_piece(PieceColor.BLACK, (0,0))
    mock_game._man_add_piece(PieceColor.BLACK, (1,5))
    mock_game._man_add_piece(PieceColor.BLACK, (4,4))
    mock_game._man_add_piece(PieceColor.BLACK, (2,2))
    mock_game._man_add_piece(PieceColor.BLACK, (2,0))
    mock_game._man_add_piece(PieceColor.RED, (4,0))

    randombot = RandomBot(mock_game, PieceColor.RED, PieceColor.BLACK)
    suggestion = randombot.suggest_move()

    assert suggestion.from_pos == (4,0) and suggestion.to_pos == (3,1)

#
# SMART TESTS
#

def test_smart_1():
    """
    Preliminary test to check if SmartBot returns
    legal move on new Checkers Board
    n = 1, PieceColor.BLACK
    """
    new_game = CheckersGame(1)

    randombot = SmartBot(new_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = randombot.suggest_move()

    assert new_game._is_move_legal(suggestion.from_pos, suggestion.to_pos)

def test_smart_2():
    """
    Checks if SmartBot promotes piece to king if possible
    n = 1, PieceColor.BLACK
    """
    mock_game = CheckersMock(1)
    mock_game._man_add_piece(PieceColor.BLACK, (2,2))
    mock_game._man_add_piece(PieceColor.RED, (1,3))

    smartbot = SmartBot(mock_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = smartbot.suggest_move()

    assert suggestion.from_pos == (2,2) and suggestion.to_pos in {(3,1), (3,3)}

def test_smart_3():
    """
    Checks if SmartBot avoids moving back pieces if possible
    n = 1, PieceColor.BLACK
    """
    mock_game = CheckersMock(1)
    mock_game._man_add_piece(PieceColor.BLACK, (1,1))
    mock_game._man_add_piece(PieceColor.BLACK, (0,2))
    mock_game._man_add_piece(PieceColor.RED, (3,1))

    smartbot = SmartBot(mock_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = smartbot.suggest_move()

    assert suggestion.from_pos == (1,1) and suggestion.to_pos in {(2,0), (2,2)}

def test_smart_4():
    """
    Checks if SmartBot captures more pieces if possible
    n = 2, PieceColor.BLACK
    """
    mock_game = CheckersMock(2)
    mock_game._man_add_piece(PieceColor.BLACK, (0,2))
    mock_game._man_add_piece(PieceColor.RED, (1,1))
    mock_game._man_add_piece(PieceColor.RED, (1,3))
    mock_game._man_add_piece(PieceColor.RED, (3,1))
    smartbot = SmartBot(mock_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = smartbot.suggest_move()
    assert (suggestion.from_pos == (0 ,2) and
            suggestion.subsequent.to_pos == (4,2))

def test_smart_5():
    """
    In the absence of winning moves,
    verifies that SmartBot chooses to promote pieces if possible.

    Situation B Description
    We assume that all pieces are pawns and not kings.

    There are two black pieces "B1, B2" and one red piece "R".
    [
        [None, None, None, None],
        [None, "B2", None, "R"],
        [None, None, "B1", None],
        [None, None, None, None]
    ]

    In this case, we can categorize the priority of the moves
    (in descending order of importance).
    Priority 1a: "B1" moves from (2,2) to (3,1)
    Priority 1b: "B1 moves from (2,2) to (3,3)
        These two moves promote "B1" to a king

    Priority 2: "B2" moves from (1,1) to (2, 0)

    n = 1, PieceColor.BLACK
    """
    mock_game = CheckersMock(1)
    mock_game._man_add_piece(PieceColor.BLACK, (1,1))
    mock_game._man_add_piece(PieceColor.BLACK, (2,2))
    mock_game._man_add_piece(PieceColor.RED, (1,3))

    smartbot = SmartBot(mock_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = smartbot.suggest_move()

    assert (suggestion.from_pos == (2,2) and
            suggestion.to_pos in {(3,3), (3,1)})

def test_smart_6():
    """
    Verifies that the Smartbot avoids moving last-row pieces

    Situation C Description:
    We assume that all pieces are pawns and not kings.

    There are two black pieces "B1, B2" and one red piece "R".
    [
        ["B1", None, None, None],
        [None, None, None, "B2"],
        [None, None, None, None],
        [None, "R", None, None]
    ]

    In this case, we can categorize the priority of the moves
    (in descending order of importance).
    Priority 1: "B2" moves from (1,3) to (2,2)
    Priority 2: "B1" moves from (0,0) to (1,1)

    n = 1, PieceColor.BLACK
    """
    mock_game = CheckersMock(1)
    mock_game._man_add_piece(PieceColor.BLACK, (1,3))
    mock_game._man_add_piece(PieceColor.BLACK, (0,0))
    mock_game._man_add_piece(PieceColor.RED, (3,1))

    smartbot = SmartBot(mock_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = smartbot.suggest_move()

    assert suggestion.from_pos == (1,3) and suggestion.to_pos == (2,2)

def test_smart_7():
    """
    Verifies that the Smartbot captures more pieces if possible

    Situation D Description:
    We assume that all pieces are pawns and not kings.

    There are two black pieces "B1", "B2" and
        four red pieces "R1", "R2", "R3", R4".
    [
        ["B1", None, None, None, None, None, None, None],
        [None, "R1", None, None, None, None, None, None],
        [None, None, None, None, "B2", None, None, None],
        [None, "R2", None, "R4", None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, "R3", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ]

    In this case, we can categorize the priority of the moves
    (in descending order of importance).
    Priority 1: "B1" moves along (0,0), (2,2), (4,0), (6,2)
        This allows the Black player to capture three pieces.
    Priority 2a: "B1" moves along (0,0), (2,2), (4,4)
    Priority 2b: "B2" moves along (2, 4), (4,2), (6,0)
        These moves allow the Black player to only capture two pieces.

    n = 3, PieceColor.BLACK
    """
    mock_game = CheckersMock(3)
    mock_game._man_add_piece(PieceColor.BLACK, (0,0))
    mock_game._man_add_piece(PieceColor.BLACK, (2,4))
    mock_game._man_add_piece(PieceColor.BLACK, (1,5))
    mock_game._man_add_piece(PieceColor.RED, (1,1))
    mock_game._man_add_piece(PieceColor.RED, (3,1))
    mock_game._man_add_piece(PieceColor.RED, (5,1))
    mock_game._man_add_piece(PieceColor.RED, (3,3))

    smartbot = SmartBot(mock_game, PieceColor.BLACK, PieceColor.RED)
    suggestion = smartbot.suggest_move()

    assert suggestion.steps_num() == 3

def test_smart_8():
    """
    Checks that Smartbot also works for the Red player
    Verifies that the Smartbot promotes a piece to king if possible

    Situation D Description:
    We assume that all pieces are pawns and not kings.

    There are two black pieces "B1", "B2" and
        four red pieces "R1", "R2", "R3", R4".
    [
        ["B1", None, None, None, None, None, None, None],
        [None, "R1", None, None, None, None, None, None],
        [None, None, None, None, "B2", None, None, None],
        [None, "R2", None, "R4", None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, "R3", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ]

    In this case, we can categorize the priority of the moves
    (in descending order of importance).
    Priority 1: "R1" moves from (1,1) to (0,2)
        This allows the red player to promote a piece
    Priority 2a: "R4" moves from (3,3) to (2,2)
    Priority 2b: "R2" moves from (3,1) to (2,0)
    Priority 2c: "R2" moves from (3,1) to (2,2)
    Priority 2d: "R3" moves from (5,1) to (4,0)
    Priority 2e: "R4" moves from (5,1) to (4,2)
        These are all general moves which are not prioritized.

    n = 3, PieceColor.RED
    """
    mock_game = CheckersMock(3)
    mock_game._man_add_piece(PieceColor.BLACK, (0,0))
    mock_game._man_add_piece(PieceColor.BLACK, (2,4))
    mock_game._man_add_piece(PieceColor.BLACK, (1,5))
    mock_game._man_add_piece(PieceColor.RED, (1,1))
    mock_game._man_add_piece(PieceColor.RED, (3,1))
    mock_game._man_add_piece(PieceColor.RED, (5,1))
    mock_game._man_add_piece(PieceColor.RED, (3,3))

    smartbot = SmartBot(mock_game, PieceColor.RED, PieceColor.BLACK)
    suggestion = smartbot.suggest_move()

    assert suggestion.from_pos == (1,1) and suggestion.to_pos == (0,2)

#
# STRATEGY TESTS
# Check if SmartBot wins more than 50% of the time
#

def test_strategy_1():
    """
    Checks that the SmartBot wins more than 50% of the time
    as the STARTING player out of 80 games where n = 3
    """
    player1 = 'smart'
    player2 = 'random'
    num_games = 80

    game = CheckersGame(3)

    bot1 = BotPlayer(player1, game, PieceColor.BLACK, PieceColor.RED)
    bot2 = BotPlayer(player2, game, PieceColor.RED, PieceColor.BLACK)

    bots = {PieceColor.BLACK: bot1, PieceColor.RED: bot2}

    simulate(game, num_games, bots)

    bot1_wins = bots[PieceColor.BLACK].wins
    bot2_wins = bots[PieceColor.RED].wins
    ties = num_games - (bot1_wins + bot2_wins)

    assert bot1_wins / num_games >= 0.5

def test_strategy_2():
    """
    Checks that the SmartBot wins more than 50% of the time
    as the SECOND player out of 80 games where n = 3
    """
    player1 = 'random'
    player2 = 'smart'
    num_games = 80

    game = CheckersGame(3)

    bot1 = BotPlayer(player1, game, PieceColor.BLACK, PieceColor.RED)
    bot2 = BotPlayer(player2, game, PieceColor.RED, PieceColor.BLACK)

    bots = {PieceColor.BLACK: bot1, PieceColor.RED: bot2}

    simulate(game, num_games, bots)

    bot1_wins = bots[PieceColor.BLACK].wins
    bot2_wins = bots[PieceColor.RED].wins
    ties = num_games - (bot1_wins + bot2_wins)

    assert bot2_wins / num_games >= 0.5
