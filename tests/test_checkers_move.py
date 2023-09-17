from checkers_move import CheckersMove
from piece import Piece
import pytest

def test_checkres_move_1():
    move_1 = CheckersMove((1,1),(2,2),None,CheckersMove((2,2),(3,3),None,
    CheckersMove((3,3),(4,4),None,CheckersMove((4,4),(5,5),None))))
    move_2 = CheckersMove((1,1),(2,2),None)
    move_2 = move_2.add_step(CheckersMove((2,2),(3,3),None))
    assert move_2.subsequent == CheckersMove((2,2),(3,3),None)
    move_2 = move_2.add_step(CheckersMove((3,3),(4,4),None))
    assert move_2.subsequent.subsequent == CheckersMove((3,3),(4,4),None)
    move_2 =  move_2.add_step(CheckersMove((4,4),(5,5),None))
    assert move_2.subsequent.subsequent.subsequent == CheckersMove((4,4),(5,5),None)
    assert move_1.steps_num() == 4
    assert move_1.steps_num() == move_2.steps_num()
    assert move_2.steps_num() == 4

def test_add_step_1():
    move = CheckersMove((1,1),(2,2),None)
    with pytest.raises(Exception, match = "from-position of the new step does "+
                                      "not match to-position of the last step"):
        move.add_step(CheckersMove((3,3),(4,4),None))

def test_remove_last_step_1():
    move = CheckersMove((1,1),(2,2),None,CheckersMove((2,2),(3,3),None,
    CheckersMove((3,3),(4,4),None)))
    move.remove_last_step()
    assert move == CheckersMove((1,1),(2,2),None,CheckersMove((2,2),(3,3),None))

def test_remove_last_step_2():
    move = CheckersMove((1,1),(2,2),None)
    move.remove_last_step()
    assert move == CheckersMove((1,1),(2,2),None)