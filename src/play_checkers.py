from logic import CheckersGame , CheckersMove , PlayerDraw
from checkers_exception import CheckersException , IncompleteMove
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
PieceType = Enum("PieceType", ["PAWN", "KING"])

def play_checkers(n):
    """
    Simulates a checkers game
    Parameter: n(int)
    Returns: None
    """
    # Create the game
    moves_lst = []
    g = CheckersGame(n)
    g._turn = g._player1
    print("When prompted, please choose positions as column # row #" + 
    "separated by space i.e. type the following to selcet second row"+
    "and third column, 2 3 ")
    play = input("press p and hit return on your keyboard to continue   ")
    while play != "p":
        play = input("press p and hit return on your keyboard to continue   ")
    # Keep playing until game is over:
    while not g._is_over:
        # Print the board
        print(g)
        current = g._turn
        piece = None
        new_pos = None
        move = None
        new_move = True #False if we are continuing a multi-step jump move
        while piece is None or new_pos is None:
            if new_move:
                old = input(f"{current}  position of piece to move> ")
                if old == "draw":
                    response = input(f"{g._get_other_player(current)}  y/n?   ")
                    if response == "y":
                        g._add_request((current , old))
                    continue
                if old == "resign":
                    g._add_request((current , old))
                    continue
                old = (int(old.split()[0]) , int(old.split()[1]))
            piece = g._get_piece(old)
            if not g._does_belong_to(old , current):
                print("This piece is not yours. Please choose a different one")
                continue
            try:
                player_valid_moves = [i for i in g._player_valid_moves(current)[piece] if 
                g._is_move_legal(i.from_pos , i.to_pos)]
            except CheckersException as e:
                print(e)
                continue
            if player_valid_moves == []:
                print("No legal moves for chosen piece")
                continue
            else:
                print(f"legal moves are {player_valid_moves}")
            if piece:
                if g._does_belong_to(old , current):
                    new = input(f"{current}  move piece to> ")
                    new =(int(new.split()[0]) , int(new.split()[1]))
                    if g._is_move_legal(old , new):
                        try:
                            g._move_piece(old , new)
                        except IncompleteMove as e:
                            g._move_no_exceptions(old , new) #lets you complete one step of a multi-step jump without erros
                            move = CheckersMove(old , new , new_pos)
                            moves_lst +=[(move.from_pos,move.to_pos)]
                            new_move = False
                            print(g)
                            print("Please complete the move")
                            old = move.to_pos
                            continue
                        except CheckersException as e:
                            print(e)
                            continue
                        new_pos = g._get_piece(new)
                        move = CheckersMove(old , new , new_pos)
                        if move:
                            moves_lst +=[(move.from_pos,move.to_pos)]
        new_move = True

         
    print(g)
    if g._winner == PlayerDraw():
        print("It is a tie")
        return
    print(f"The winner is {g._winner}!")
   # print(moves_lst) #print list of moves used in the game to use for tests
    return 

if __name__ == "__main__":
    play_checkers(2)

