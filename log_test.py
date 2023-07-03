import random

import pygame.font

from chess_engine import GameState
import pygame as py
from chess_gui import load_images, draw_game_state
from enums import EPlayer
from logger import ChessLogger

"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray")]
test_logger = ChessLogger(__name__, "tests.log")

game = GameState()
py.init()
screen = py.display.set_mode((WIDTH, HEIGHT))
clock = py.time.Clock()
load_images()
font = pygame.font.Font(None, 30)
square_selected = ()
running = True
valid_moves = []
game_over = False


def play_game():

    try:
        while game.checkmate_stalemate_checker() > 2:
            pygame.event.pump()
            # Generate a random move for the current player
            piece, move = generate_random_move(game)
            draw_game_state(screen, game, valid_moves, piece.get_pos())
            current_player = 'white' if game.whose_turn() else 'black'
            window_log(f"Player {current_player} moves: {piece.__str__()} to {move}")
            game.move_piece(piece.get_pos(), move, True)

            clock.tick(MAX_FPS)
            py.display.flip()
        test_logger.log_board(game.board)
        print("Game over.")
        print("Result:", game.checkmate_stalemate_checker())
    except Exception as e:
        print(e)
        test_logger.log_board(game.board)


def generate_random_move(game_state):
    valids = []
    piece = None
    pieces = game.pieces[game_state.whose_turn()][:]
    takes = pieces[:]
    while bool(takes):
        piece = random.choice(takes)
        take_moves = piece.get_valid_piece_takes(game_state)
        if bool(take_moves):
            valids += take_moves
        takes.remove(piece)
    while bool(pieces):
        piece = random.choice(pieces)
        moves = game_state.get_valid_moves(piece.get_pos())
        if bool(moves):
            valids += moves
            break
        pieces.remove(piece)
    return piece, random.choice(valids)


play_game()


def print_board(board):
    for row in board:
        print("---------------------------------\n")
        print("| ")
        for col in row:
            if col == -9:
                print("|   ")
            elif col.get_player() == EPlayer.PLAYER_1:
                print("| " + col.get_name().upper() + " ")
            else:
                print("| " + col.get_name() + " ")
            print((" " if col == -9 else col.get_name()) + " | ", end="")
        print()
    print("---------------------------------\n")


def window_log(info, y=10, x=10):
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, 'magenta')
    debug_rect = debug_surface.get_rect(topleft=(x, y))
    display_surface.blit(debug_surface, debug_rect)


play_game()
