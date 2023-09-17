from logic import CheckersGame , PlayerDraw
from checkers_exception import CheckersException , IncompleteMove
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
PieceType = Enum("PieceType", ["PAWN", "KING"])
from checkers_move import CheckersMove
import pytest

def test_winner_1():
    g = CheckersGame(1)
    
    moves = [((0,0),(1,1)),((3,1),(2,2)),((1,1),(2,0)),((2,2),(1,3)),
    ((2,0),(3,1)),((3,3),(2,2)),((3,1),(2,0)),((2,2),(1,1)),((2,0),(3,1)),
    ((1,1),(0,0)),((3,1),(2,0)),((0,0),(1,1)),((2,0),(3,1)),((1,1),(2,0)),
    ((3,1),(2,2)),((2,0),(3,1)),((2,2),(3,3)),((3,1),(2,0)),((3,3),(2,2)),
    ((2,0),(1,1)),((2,2),(0,0))]
    
    for move in moves:
        g._move_piece(move[0] , move[1])
    assert g._is_over == True
    assert g._get_winner() == g._player1

def test_winner_2():
    g = CheckersGame(2)

    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)),((1,3),(3,1)),((3, 1), (5, 3)), ((5, 1), (4, 2)), 
    ((5, 3), (3, 5)), ((5, 5), (4, 4)), ((3,5),(5,3)), ((5, 3), (3, 1))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    assert g._is_over == True
    assert g._player2._pieces == set()
    assert g._get_winner() == g._player1

def test_winner_3():
    g = CheckersGame(2)

    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)),
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)), ((1, 3), (3, 1)), ((3, 1), (5, 3)), ((4, 4), (3, 5)),
    ((5, 3), (4, 4)), ((5, 5), (3, 3)), ((2, 4), (4, 2)), ((5, 1), (3, 3)),
    ((1, 5), (2, 4)), ((3, 3), (1, 5)), ((0, 0), (1, 1)), ((3, 5), (2, 4)),
    ((0, 4), (1, 3)), ((2, 4), (0, 2)), ((1, 1), (2, 2)), ((1, 5), (0, 4)),
    ((2, 2), (3, 3)), ((0, 2), (1, 3)), ((3, 3), (4, 4)), ((1, 3), (2, 4)),
    ((4, 4), (5, 3)), ((2, 4), (3, 5)), ((5, 3), (4, 2)), ((0, 4), (1, 5)),
    ((4, 2), (5, 3)), ((1, 5), (2, 4)), ((5, 3), (4, 4)), ((3, 5), (5, 3)),
    ((4, 0), (5, 1)), ((5, 3), (4, 2)), ((5, 1), (3, 3)), ((3, 3), (1, 5))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    assert g._is_over == True
    assert g._player2._pieces == set()
    assert g._get_winner() == g._player1

def test_winner_4():
    g = CheckersGame(2)

    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)),
    ((4, 2), (3, 3)), ((1, 3), (2, 2)), ((3, 3), (1, 1)), ((0, 2), (2, 0)),
    ((4, 4), (3, 3)), ((1, 5), (2, 4)), ((3, 3), (1, 5)), ((0, 4), (1, 3)),
    ((1, 5), (0, 4)), ((0, 0), (1, 1)), ((0, 4), (2, 2)), ((2, 2), (0, 0)),
    ((2, 0), (3, 1)), ((5, 3), (4, 2)), ((3, 1), (5, 3)), ((5, 1), (4, 2)),
    ((5, 3), (3, 1)), ((5, 5), (4, 4)), ((4, 0), (5, 1)), ((4, 4), (3, 3)),
    ((3, 1), (2, 2)), ((3, 3), (1, 1)), ((5, 1), (4, 2)), ((1, 1), (0, 2)),
    ((4, 2), (3, 3)), ((0, 0), (1, 1)), ((3, 3), (2, 2)), ((1, 1), (3, 3))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    assert g._is_over == True
    assert g._player1._pieces == set()
    assert len(g._player2._pieces) == 2
    assert g._get_winner() == g._player2

def test_no_winner_1():
    g = CheckersGame(3)
    assert g._is_over == False
    assert g._get_winner() == None

def test_no_winner_2():
    g = CheckersGame(1)
    
    moves = [((0,0),(1,1)),((3,1),(2,2)),((1,1),(2,0)),((2,2),(1,3)),
    ((2,0),(3,1)),((3,3),(2,2)),((3,1),(2,0)),((2,2),(1,1)),((2,0),(3,1)),
    ((1,1),(0,0)),((3,1),(2,0)),((0,0),(1,1)),((2,0),(3,1)),((1,1),(2,0)),
    ((3,1),(2,2)),((2,0),(3,1)),((2,2),(3,3))]
    
    for move in moves:
        g._move_piece(move[0] , move[1])
    assert g._is_over == False
    assert g._get_winner() == None

def test_piece_pos_1():
    g = CheckersGame(2)
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)),((1,3),(3,1)),((3, 1), (5, 3)), ((5, 1), (4, 2)), 
    ((5, 3), (3, 5)), ((5, 5), (4, 4)), ((3,5),(5,3)), ((5, 3), (3, 1))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    assert g._get_piece((0,0))._pos == (0,0)
    assert g._get_piece((0,4))._pos == (0,4) 
    assert g._get_piece((3,1))._pos == (3,1) 
    
def test_piece_type_1():
    g = CheckersGame(2)
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)),((1,3),(3,1)),((3, 1), (5, 3)), ((5, 1), (4, 2)), 
    ((5, 3), (3, 5)), ((5, 5), (4, 4)), ((3,5),(5,3)), ((5, 3), (3, 1))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    assert g._get_piece((0,0)) is not None
    assert g._get_piece((0,4)) is not None
    assert g._get_piece((3,1)) is not None
    assert g._get_piece((0,0))._piece_type.value == PieceType.PAWN.value
    assert g._get_piece((0,4))._piece_type.value == PieceType.PAWN.value
    assert g._get_piece((3,1))._piece_type.value == PieceType.KING.value
    assert g._get_piece((0,0))._color.value == PieceColor.BLACK.value
    assert g._get_piece((0,4))._color.value == PieceColor.BLACK.value
    assert g._get_piece((3,1))._color.value == PieceColor.BLACK.value


def test_player_moves_1():
    g = CheckersGame(2)
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2))]
    
    for move in moves:
        g._move_piece(move[0] , move[1])
    correct_move = [CheckersMove((1,3),(3,1),g._get_piece((1,3)),
                   CheckersMove((3,1),(5,3),g._get_piece((1,3))))]
    assert g._player_valid_moves(g._player1)[g._get_piece((1,3))] == correct_move
    with pytest.raises(CheckersException , match = "Jump must be done when avaliable"):
        g._is_move_legal((0,0) , (1,1))

def test_player_moves_2():
    g = CheckersGame(2)
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2))]
    
    for move in moves:
        g._move_piece(move[0] , move[1])
    with pytest.raises(CheckersException , match = "Jump must be done when avaliable"):
        g._is_move_legal((0,4) , (1,3))

def test_player_moves_3():
    g = CheckersGame(2)
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2))]
    
    for move in moves:
        g._move_piece(move[0] , move[1])
    with pytest.raises(CheckersException , match = "No piece at given position"):
        g._move_piece((0,1) , (1,2))

def test_player_moves_4():
    g = CheckersGame(2)
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3))]
    
    for move in moves:
        g._move_piece(move[0] , move[1])
    with pytest.raises(CheckersException , match = "Invalid move"):
        g._move_piece((4,4) , (3,3))

def test_turn_1():
    g = CheckersGame(2)
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2))]
    
    for move in moves:
        g._move_piece(move[0] , move[1])
    assert g._turn == g._player1

def test_turn_2():
    g = CheckersGame(2)
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3))]
    
    for move in moves:
        g._move_piece(move[0] , move[1])
    assert g._turn == g._player2

def test_kinging_1():
    g = CheckersGame(2)

    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)),((1,3),(3,1)),((3, 1), (5, 3))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    assert g._get_piece((5,3)) is not None
    assert g._get_piece((5,3))._piece_type.value == PieceType.KING.value

def test_kinging_2():
    g = CheckersGame(2)

    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)),((1,3),(3,1)),((3, 1), (5, 3)), ((5, 1), (4, 2)), 
    ((5, 3), (3, 5))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    assert g._get_piece((3,5)) is not None
    assert g._get_piece((3,5))._piece_type.value == PieceType.KING.value

def test__move_piece_func_1():
    try:
        game = CheckersGame(2)
        game._move_piece((1,3), (2,4))
        game._move_piece((4,0), (3,1))
        game._move_piece((1,1), (2,0))
        game._move_piece((4,4), (3,5))
        game._move_piece((2,4), (3,3))
        game._move_piece((4,2), (2,4))
        game._move_piece((1,5), (3,3))
        game._move_piece((3,1), (2,2))
        game._move_piece((3,3), (4,2))
        game._move_piece((5,1), (3,3))
        game._move_piece((2,0), (3,1))
        game._move_piece((3,5), (2,4))
        game._move_piece((3,1), (4,2))
        game._move_piece((5,3), (3,1))
        game._move_piece((0,2), (1,1))
        game._move_piece((2,2), (1,3))
    except Exception as e:
        assert False, f"raised{e}"

def test__move_checkers_func_1():
    try:
        game = CheckersGame(2)
        game._move_piece((1,3), (2,4))
        game._move_piece((4,0), (3,1))
        game._move_piece((1,1), (2,0))
        game._move_piece((4,4), (3,5))
        game._move_piece((2,4), (3,3))
        game._move_piece((4,2), (2,4))
        game._move_piece((1,5), (3,3))
        game._move_piece((3,1), (2,2))
        game._move_piece((3,3), (4,2))
        game._move_piece((5,1), (3,3))
        game._move_piece((2,0), (3,1))
        game._move_piece((3,5), (2,4))
        game._move_piece((3,1), (4,2))
        game._move_piece((5,3), (3,1))
        game._move_piece((0,2), (1,1))
        move = game._piece_valid_moves((2,2))[0]
        game._move_checkers(move)
    except Exception as e:
        assert False, f"raised{e}"
    
def test_resign_1():
    g = CheckersGame(2)

    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)),((1,3),(3,1)),((3, 1), (5, 3)), ((5, 1), (4, 2))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    p = g._turn
    g._add_request((p,"resign"))
    g._move_piece((5, 3), (3, 5))
    assert g._is_over
    assert g._winner == g._get_other_player(p)

def test_resign_2():
    g = CheckersGame(2)
    g._add_request((g._player1,"resign"))
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)),((1,3),(3,1)),((3, 1), (5, 3)), ((5, 1), (4, 2))]
    
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    g._move_piece((5, 3), (3, 5))
    assert g._is_over
    assert g._winner == g._player2

def test_draw_1():
    g = CheckersGame(2)
    g._add_request((g._player1,"draw"))
    moves = [((1, 1), (2, 2)), ((4, 0), (3, 1)), ((2, 2), (4, 0)), 
    ((4, 2), (3, 3)), ((1, 3), (2, 4)), ((5, 3), (4, 2)), ((0, 2), (1, 3)),
    ((3, 3), (2, 2)),((1,3),(3,1)),((3, 1), (5, 3)), ((5, 1), (4, 2))]
    for move in moves:
        try:
            g._move_piece(move[0] , move[1])
        except IncompleteMove:
            g._move_no_exceptions(move[0] , move[1])
    g._move_piece((5, 3), (3, 5))
    assert g._is_over
    assert g._winner == PlayerDraw()