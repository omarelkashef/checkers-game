import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import click
from player import Player
from board import Board
from piece import Piece
from checkers_move import CheckersMove
from checkers_exception import CheckersException , IncompleteMove
from logic import CheckersGame

from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
PieceType = Enum("PieceType", ["PAWN", "KING"])
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (60,179,113)
RED = (255, 0, 0)
YELLOW = (255, 192, 0)
WIDTH = 650
HEIGHT = 600
TEXT = {0:'Welcome! Press <s> to start game.',
        1: "Choose positions as <row#+SPACE+column#> using your keyboard",
        2: 'Select a Piece',
        3:'',
        4: "Press <p> to continue",
        6: 'Select a move',
        7: "Press <m> to continue",
        8: 'Not valid piece, select again',
        9: 'No moves available for this piece, select again',
       10: 'Move is not valid, select again',
       11: 'You must exhaust all jumps',
       12: 'Must jump, select again'}

def print_text(string):
    """
    Helper function to print text boxes needed on the screen
    """
    font = pygame.font.SysFont('menlo', 16)
    text = font.render(string, True, BLACK)
    textRect =text.get_rect()
    return text, textRect

def draw_board(surface,Game,d=None):
    """
    Draws all components of the board:
    - the checker board itself
    - pieces
    - possible locations to move (if applicable)
    - current player
    - winner (if applicable)
    """
    grid = Game._state._grid
    nrows = len(grid)+1
    ncols = len(grid[0])+1
    surface.fill(GREEN)
    rh = HEIGHT // nrows + 1
    cw = WIDTH // ncols + 1
        
    def rectangles(color, rect, width):
        """
        Helper function to draw rectangles
        """
        pygame.draw.rect(surface, color=color,rect=rect, width=width)
    # Draw the borders around each cell
    for row in range(nrows-1):
        for col in range(ncols-1):
            rect = (col * cw, row * rh, cw, rh)
            if (row+col)%2 == 0:
                rectangles(WHITE,rect,0)
            else:
                rectangles(WHITE,rect,2)
            #if piece is selected, shows possible moves as highlighted cells
            if (d != None) and (row in d.keys()) and (col in d[row]): 
                rectangles(YELLOW,rect,5)
                
    #print current turn on screen
    cp = print_text(f'Current player:{str(Game._turn)}')
    cp[1].center = (WIDTH // 2, HEIGHT+20)
    surface.blit(cp[0],cp[1])

    def rc_helper(center,n):
        """
        Helps print the row and column numbers on the side of the grid.
        """
        c = print_text(str(n))
        c[1].center = center
        surface.blit(c[0],c[1])
    # Print row and column numbers
    for i, r in enumerate(grid): 
        for j, piece in enumerate(r):
            if i == len(grid)-1:
                center = (j * cw + cw // 2, (i+1) * rh + rh // 2)
                rc_helper(center,j)
            if j == len(grid[0])-1:
                center = ((j+1) * cw + cw // 2, i * rh + rh // 2)
                rc_helper(center,i)
            #now print circles if a piece is in the cell of the grid
            center = (j * cw + cw // 2, i * rh + rh // 2)
            if piece is None:
                pass
            else:
                if piece._color.value == 1:
                    color = "RED"
                else:
                    color = "BLACK"
                if piece._piece_type.value == 1:
                    k = 1
                else:
                    k = 2
                radius = rh // 2 - 8
                pygame.draw.circle(surface, color = color,
                                center=center, radius=radius)
                if k == 2:
                    pygame.draw.circle(surface, color=YELLOW,
                                center=center, radius=radius//2)
        

def play_checkers(Game):
    """
    Main part of code that runs the GUI.
    """
    pygame.init()
    pygame.display.set_caption("CHECKERS")
    surface = pygame.display.set_mode((WIDTH+10,HEIGHT+100))
    t = [0,1]
    p = (None,None)
    n = (None,None)
    coord = ''
    clock = pygame.time.Clock()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    while not Game._is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == 115: #<s> game started, initilaize game on screen
                    t = [2,4]
                if event.unicode in '0123456789': #save coordinate input from user
                    coord += event.unicode
                if event.key == 32:
                    coord += ' '
                if event.key == 112: #<p> for piece was just selected
                    #if move is not valid, show error and clear the coord
                    p = (tuple([int(x) for x in coord.split()]))
                    if not Game._does_belong_to(p,Game._turn):
                        p = (None,None)
                        t = [8,4]
                    else:
                        try: 
                            get_to_pos(Game,p)[1]
                            if len(get_to_pos(Game,p)[1]) == 0:
                                p = (None,None)
                                t = [9,4]
                            else:    
                                TEXT[3] = temp(p)
                                t = [6, 3, 7]
                        except CheckersException:
                            p = (None,None)
                            t = [12, 4]
                    coord = ''
                if event.key == 109: #<m> for move was just selected
                    #if move is not valid, show error and clear the coord
                    n = (tuple([int(x) for x in coord.split()]))
                    if not n in get_to_pos(Game,p)[1]:
                        n = (None,None)
                        t = [10,7]
                    else:
                        TEXT[3] = 'Last move is:' + temp(p,n)
                        try:
                            Game._move_piece(p , n)
                            p = (None,None)
                            n = (None,None)
                            t = [2,3,4]
                        except IncompleteMove:
                            print('three')
                            Game._move_no_exceptions(p , n)
                            p = n
                            t = [11,6,7]
                    coord = ''
        d = get_to_pos(Game,p)[0]
        draw_board(surface,Game,d)
        #print texts needed for next step of the game
        for i , textind in enumerate(t):
            c = print_text(TEXT[textind])
            c[1].center = (WIDTH // 2, HEIGHT+55+i*18)
            surface.blit(c[0],c[1])
        pygame.display.flip()
        clock.tick(24)
    #the game is over
    draw_board(surface, Game)
    winner = Game._get_winner()
    if winner is not None:
        c = print_text(f'GAME OVER! WINNER IS:{winner}')
    else:
        c = print_text('GAME OVER! ITS A TIE')
    c[1].center = (WIDTH // 2, HEIGHT+55)
    surface.blit(c[0],c[1])
    pygame.display.flip()
    clock.tick(2)

def temp(p=None,n=None):
    """
    Helper function for string representing the selected piece and location to move.
    """
    return f"Selected Piece :{p}   Move to: {n}"

def get_to_pos(Game,p):
    """
    Finds cells that piece p can move to.
    """
    if p == (None,None):
        return (None,None)
    piece = Game._get_piece(p)
    x = [i.to_pos for i in Game._player_valid_moves(Game._turn)[piece] if 
            Game._is_move_legal(i.from_pos , i.to_pos)]
            #gets error here, need to find a way to find moves without jumps, and if jump is needed, tell them later?
    y = x+[p]
    d = {}
    for loc in y:
        d[loc[0]] = d.get(loc[0],[])+[loc[1]]
    return d,x

@click.command(name = "checkers-gui")
@click.option('--size', type = click.INT, default = 2)

def cmd(size):
    game = CheckersGame(size)
    play_checkers(game)

if __name__ == "__main__":
    cmd()
