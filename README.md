# project-jhryu-leemichael-kshar-omarelk

This repository contains a design and implementation for Checkers. 
The group members are

- Omar Elkashef: Game Logic
- Irene Ryu: GUI
- Karim Sharaf: TUI
- Michael Lee: Bot

# Setup

Running the code in this repository requires using a number of
Python libraries. We recommend creating a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
before installing these libraries. To do so, run the
following from the root of your local repository:

    python3 -m venv venv

To activate your virtual environment, run the following:

    source venv/bin/activate

You should now see `(venv)` in your terminal prompt, indicating
that the virtual environment is active.

Navigate to the project directory by running

    cd project-jhryu-leemichael-kshar-omarelk

To install the required Python libraries run the following:

    pip3 install -r requirements.txt

To deactivate the virtual environment, just run the following:

    deactivate
You can run a simple TUI in using 
    
    python3 src/play_checkers.py
    
# Changes from Milestone 1 (Design Feedback) 
1) Separated Checkers specific logic from Board class by adding a CheckersGame
class that has all the logic and made a Board class game-agnostic and support
arbitrary rectangular sizes.
2) Added CheckersMove class since a move is a complicated action. It stores
from-position, to-position, piece carrying the move and subsequent moves. It 
also has useful methods that check if a move promotes a piece to a king for 
example.
3) Removed idnum attribute from Piece class

# Changes from Milestone 2 (Initial Implementation)
## TUI
To run the TUI, run the following from the root of the repository:

``python3 src/tui.py``

Please view the ``tui_Simulation.ipynb`` file for a game simulation to make sure you understand the diffrent game inputs

- Notes:
1) Keep in mind that the Red player's king will be represnted as a Green Piece and the Black player's king will be represneted as a Yellow piece
2) When inputing color or opponent player type please make sure to write in uppercase

-Addressing Feedback:
1) It now supports board sizes from 6x6 to 20x20
-Other Changes:
1) TUI is currently fully functional and integrated with game logic and bots. It is capable of running a full game between a human and a randombot or a human and a smart bot or a human and another human on the same computer. 

## GUI
To run the GUI, run the following from the root of the repository:

    ``python3 src/gui.py``

Default board size is set as 6x6 but this can be changed to an nxn board size by running
    
    ''python3 src/gui.py --size n''

- Feedback: unable to run GUI --> resolved through testing
- Implemention requirements from Milestone 2 are fulfilled.
- Make sure to click the correct sequence of values as prompted by the screen, otherwise may run into errors.
    - **p:** after piece selection
    - **m:**: after move selection
    - **row#+SPACE+column#:** fixed format for piece selection input
- resignation and draws are not supported

## Bots

Since Milestone 2, the bot is now integrated with the game logic and TUI.
We can now run simulations to test the success rate of the SmartBot's strategy.

The ``bot.py`` file includes three classes:

- ``Bot``: An abstract base class for the ``RandomBot`` and ``SmartBot``
- ``RandomBot``: A bot that will just choose a move at random
- ``SmartBot``: Implements the following strategies in the 
    specified order of priority: 
    1. Carry out a winning move if it exists
    2. Promote a piece to king if possible
    3. Capture more rather than fewer pieces if the player must capture
    4. Avoid moving the back row pieces
        (only move the back row if no other move is possible)

You can run``bot.py`` to run 100 simulated games where two bots face 
each other, and see the percentage of wins and ties. For example:

    $ python3 src/bot.py --player1 random --player2 random
    Bot 1 (random) wins: 51.00%
    Bot 2 (random) wins: 49.00%
    Ties: 0.00%
    
    $ python3 src/bot.py --player1 random --player2 smart
    Bot 1 (random) wins: 31.00%
    Bot 2 (smart) wins: 69.00%
    Ties: 0.00%

You can control the number of simulated games using the ``-n <number of games>`` 
parameter to ``bot.py``.

The ``test_bot.py`` file contains the extended descriptions of testing 
situations over two strategy tests, four random tests and eight smart tests. 

- The strategy tests check that a SmartBot wins more than 50% of the time when 
playing against a RandomBot in games where n = 3, regardless of whether it is
the starting or second player.

- The smart and random tests present the bots with various board states 
(created with the ``CheckersMock`` class in ``bots_mock.py``) and 
evaluate if they return a desired or valid move.

Run the following command from the root of the repository first:

    export PYTHONPATH=$(pwd)/src    

Then, the automated tests can be run like this:

    pytest -v tests/test_bot.py

## Game Logic 

-Addressing Feedback:
1) Updated design to reflect final design of game logic
2) _get_winner() only checks whether there are available moves or not since no
pieces is a special case of that condition and same with _is_game_over()
3) Changed _get_pos_in_dir() docstrings to reflect that fact that it can 
return empty tuple
4) Changed _get_jumps() docstrings to reflect the fact that it takes a list of 
diagonal directions not just one direction

-Other Changes:
1) Moved _move_wins() from CheckersGame to bot file
2) Instead of only having _move_piece() function in logic.py, now we have
_move_piece() that is the same but uses a helper function _move_no_exceptions()
that moves a piece without raising any excptions. There is also _move_checkers()
that supports multi-steps moves and CheckersMove objects as inputs.
3) Added tests for logic and CheckersMove
4) Added requesting a draw and resignation functionality: a player can request
a draw or resignation at anytime but the request will be processed only when it 
legal to do so. The requests are processed in the order they are added then 
according to whether it is legal to perform them at the moment or not.

Automated tests can be run like this from the root to test various game logic scenarios:

    pytest -v tests/test_logic.py

Or, to test CheckersMove class, run this from the root:
    
    pytest -v tests/test_checkers_move.py


