#
# The Chess Board class
# Will store the state of the chess game, print the chess board, find valid moves, store move logs.
#
# Note: move log class inspired by Eddie Sharick
#
import numpy as np
from Piece import Rook, Knight, Bishop, Queen, King, Pawn
from chess_move import ChessMove, CastleMove, EnPassantMove, PawnPromotionMove, TwoSquarePawnMove
from enums import EPlayer, PieceDirection
from logger import ChessLogger

engine_logger = ChessLogger(__name__, file="engine_logs.log", h="console")
'''
r \\ c     0           1           2           3           4           5           6           7 
0   [(r=0, c=0), (r=0, c=1), (r=0, c=2), (r=0, c=3), (r=0, c=4), (r=0, c=5), (r=0, c=6), (r=0, c=7)]
1   [(r=1, c=0), (r=1, c=1), (r=1, c=2), (r=1, c=3), (r=1, c=4), (r=1, c=5), (r=1, c=6), (r=1, c=7)]
2   [(r=2, c=0), (r=2, c=1), (r=2, c=2), (r=2, c=3), (r=2, c=4), (r=2, c=5), (r=2, c=6), (r=2, c=7)]
3   [(r=3, c=0), (r=3, c=1), (r=3, c=2), (r=3, c=3), (r=3, c=4), (r=3, c=5), (r=3, c=6), (r=3, c=7)]
4   [(r=4, c=0), (r=4, c=1), (r=4, c=2), (r=4, c=3), (r=4, c=4), (r=4, c=5), (r=4, c=6), (r=4, c=7)]
5   [(r=5, c=0), (r=5, c=1), (r=5, c=2), (r=5, c=3), (r=5, c=4), (r=5, c=5), (r=5, c=6), (r=5, c=7)]
6   [(r=6, c=0), (r=6, c=1), (r=6, c=2), (r=6, c=3), (r=6, c=4), (r=6, c=5), (r=6, c=6), (r=6, c=7)]
7   [(r=7, c=0), (r=7, c=1), (r=7, c=2), (r=7, c=3), (r=7, c=4), (r=7, c=5), (r=7, c=6), (r=7, c=7)]
'''


# TODO: Flip the board according to the player
# TODO: Pawns are usually indicated by no letters
# TODO: stalemate
# TODO: change move method argument about is_ai into something more elegant
def is_valid_square(row, col):
    return (0 <= row < 8) and (0 <= col < 8)


class GameState:
    # Initialize 2D array to represent the chess board
    def __init__(self):
        self.text = 0
        self.player_stats = {
            EPlayer.PLAYER_1: {
                'pieces': 16,
                'captured': 0,
                'check': False,
                'checkmate': False,
                'stalemate': False,
                'king_location': (0, 4),
                'can_castle': [True, True, True],
                'valid_moves': []
            },
            EPlayer.PLAYER_2: {
                'pieces': 16,
                'captured': 0,
                'check': False,
                'checkmate': False,
                'stalemate': False,
                'king_location': (7, 4),
                'can_castle': [True, True, True],
                'valid_moves': []
            }
        }
        self._all_valid_moves = {}
        self.moves = 0
        self.move_log = []
        self.white_turn = True
        self.can_en_passant_bool = False
        self.en_passant_previous = (-1, -1)
        self.checkmate = False
        self.stalemate = False

        self._is_check = False

        # Initialize White pieces
        white_rook_1 = Rook('r', 0, 0, EPlayer.PLAYER_1)
        white_rook_2 = Rook('r', 0, 7, EPlayer.PLAYER_1)
        white_knight_1 = Knight('n', 0, 1, EPlayer.PLAYER_1)
        white_knight_2 = Knight('n', 0, 6, EPlayer.PLAYER_1)
        white_bishop_1 = Bishop('b', 0, 2, EPlayer.PLAYER_1)
        white_bishop_2 = Bishop('b', 0, 5, EPlayer.PLAYER_1)
        white_queen = Queen('q', 0, 3, EPlayer.PLAYER_1)
        white_king = King('k', 0, 4, EPlayer.PLAYER_1)
        white_pawn_1 = Pawn('p', 1, 0, EPlayer.PLAYER_1)
        white_pawn_2 = Pawn('p', 1, 1, EPlayer.PLAYER_1)
        white_pawn_3 = Pawn('p', 1, 2, EPlayer.PLAYER_1)
        white_pawn_4 = Pawn('p', 1, 3, EPlayer.PLAYER_1)
        white_pawn_5 = Pawn('p', 1, 4, EPlayer.PLAYER_1)
        white_pawn_6 = Pawn('p', 1, 5, EPlayer.PLAYER_1)
        white_pawn_7 = Pawn('p', 1, 6, EPlayer.PLAYER_1)
        white_pawn_8 = Pawn('p', 1, 7, EPlayer.PLAYER_1)

        # Initialize Black Pieces
        black_rook_1 = Rook('r', 7, 0, EPlayer.PLAYER_2)
        black_rook_2 = Rook('r', 7, 7, EPlayer.PLAYER_2)
        black_knight_1 = Knight('n', 7, 1, EPlayer.PLAYER_2)
        black_knight_2 = Knight('n', 7, 6, EPlayer.PLAYER_2)
        black_bishop_1 = Bishop('b', 7, 2, EPlayer.PLAYER_2)
        black_bishop_2 = Bishop('b', 7, 5, EPlayer.PLAYER_2)
        black_queen = Queen('q', 7, 3, EPlayer.PLAYER_2)
        black_king = King('k', 7, 4, EPlayer.PLAYER_2)
        black_pawn_1 = Pawn('p', 6, 0, EPlayer.PLAYER_2)
        black_pawn_2 = Pawn('p', 6, 1, EPlayer.PLAYER_2)
        black_pawn_3 = Pawn('p', 6, 2, EPlayer.PLAYER_2)
        black_pawn_4 = Pawn('p', 6, 3, EPlayer.PLAYER_2)
        black_pawn_5 = Pawn('p', 6, 4, EPlayer.PLAYER_2)
        black_pawn_6 = Pawn('p', 6, 5, EPlayer.PLAYER_2)
        black_pawn_7 = Pawn('p', 6, 6, EPlayer.PLAYER_2)
        black_pawn_8 = Pawn('p', 6, 7, EPlayer.PLAYER_2)

        self.board = np.array([
            [white_rook_1, white_knight_1, white_bishop_1, white_queen, white_king, white_bishop_2, white_knight_2,
             white_rook_2],
            [white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5, white_pawn_6, white_pawn_7,
             white_pawn_8],
            np.full(8, EPlayer.EMPTY),
            np.full(8, EPlayer.EMPTY),
            np.full(8, EPlayer.EMPTY),
            np.full(8, EPlayer.EMPTY),
            [black_pawn_1, black_pawn_2, black_pawn_3, black_pawn_4, black_pawn_5, black_pawn_6, black_pawn_7,
             black_pawn_8],
            [black_rook_1, black_knight_1, black_bishop_1, black_queen, black_king, black_bishop_2, black_knight_2,
             black_rook_2]
        ])

    def get_piece(self, row, col):
        if (0 <= row < 8) and (0 <= col < 8):
            return self.board[row, col]
        else:
            return None

    def is_valid_piece(self, row, col):
        evaluated_piece = self.get_piece(row, col)
        return (evaluated_piece is not None) and (evaluated_piece != EPlayer.EMPTY)

    def get_valid_moves(self, starting_square: tuple[int, int]):
        def is_point_on_line(point, start, end):
            y, x = point
            y1, x1 = start
            y2, x2 = end
            if x1 != x2:
                slope = (y2 - y1) / (x2 - x1)
                y_intercept = y1 - slope * x1
                on_line = y == slope * x + y_intercept and min(y1, y2) <= y <= max(y1, y2)

            else:
                on_line = min(y1, y2) <= y <= max(y1, y2) and x == x1

            return on_line and point != start

        # # check if valid moves is empty
        # if bool(self._valid_moves):
        #     pass

        if not self.is_valid_piece(*starting_square):
            return None

        moving_piece = self.board[starting_square]
        player = moving_piece.get_player()
        king_location = self.player_stats[player]["king_location"]
        pins_check, checking_pieces, pinned_pieces = self.check_for_check(king_location, player)
        initial_valid_piece_moves = moving_piece.get_valid_piece_moves(self)

        if not pinned_pieces and not checking_pieces and not moving_piece.get_name() == "k":
            return initial_valid_piece_moves

        # if the piece is pinned, and the piece is not the king, and the king is not in check
        if pinned_pieces and not checking_pieces and len(pinned_pieces) == 1:
            if starting_square in pinned_pieces:
                # return all moves in that direction
                return [move for move in initial_valid_piece_moves
                        if is_point_on_line(move, king_location, starting_square)]

            # if the moving piece is not the one pinning the king, and not the king itself, than it can move anywhere
            elif moving_piece.get_name() != "k":
                return initial_valid_piece_moves

        # if the piece is checking the king, it can only move to block the check or capture the checking piece
        if checking_pieces and starting_square not in pinned_pieces \
                and len(checking_pieces) == 1 and moving_piece.get_name() != "k":
            return [move for move in initial_valid_piece_moves
                    if is_point_on_line(move, king_location, checking_pieces[0])]

        return [move for move in initial_valid_piece_moves if self.try_moving_piece(starting_square, move, player)]

    def try_moving_piece(self, starting_square, ending_square, player):
        temp = self.board[starting_square]
        temp2 = self.board[ending_square]

        self.board[starting_square] = EPlayer.EMPTY
        self.board[ending_square] = temp

        if temp.get_name() == "k":
            self.player_stats[player]["king_location"] = ending_square

        is_check = self.check_for_check(ending_square, player)[1]
        self.board[starting_square] = temp
        self.board[ending_square] = temp2
        if temp.get_name() == "k":
            self.player_stats[player]["king_location"] = starting_square
        return not is_check

    # 0 if white lost, 1 if black lost, 2 if stalemate, 3 if not game over
    def checkmate_stalemate_checker(self):

        all_white_moves = self.get_all_legal_moves(EPlayer.PLAYER_1)
        all_black_moves = self.get_all_legal_moves(EPlayer.PLAYER_2)

        black_checkmate = self.player_stats[EPlayer.PLAYER_2]["in_check"] and not \
            self.player_stats[EPlayer.PLAYER_2]["valid_moves"] and not self.white_turn
        white_checkmate = self.player_stats[EPlayer.PLAYER_1]["in_check"] and not\
            self.player_stats[EPlayer.PLAYER_1]["valid_moves"] and self.white_turn

        if white_checkmate:
            return 0
        elif black_checkmate:
            return 1
        elif not all_white_moves and not all_black_moves:
            return 2
        else:
            return 3

    def get_all_legal_moves(self, player):
        if not bool(self.player_stats[player]["valid_moves"]):
            self.player_stats[player]["valid_moves"] = [
                (piece.get_pos(), move)
                for row in self.board
                for piece in row if piece != EPlayer.EMPTY and piece.is_player(player)
                for move in self.get_valid_moves(piece.get_pos())
            ]
        return self.player_stats[player]["valid_moves"]

    def can_castle(self, player, rng, rook_indexes):
        castle_state = self.player_stats[player]["can_castle"]
        row, col = self.player_stats[player]["king_location"]
        if self.player_stats[player]["in_check"]:
            return False
        for i in range(*rng):
            if self.get_piece(row, col - i) != EPlayer.EMPTY:
                return False
        return castle_state[0] and castle_state[rook_indexes[0]] and \
            self.get_piece(row, rook_indexes[1]) is EPlayer.EMPTY

    def king_can_castle_left(self, player):
        return self.can_castle(player, (1, 3), (1, 1))

    def king_can_castle_right(self, player):
        return self.can_castle(player, (-1, -3, -1), (2, 6))

    def can_en_passant(self, current_square_row, current_square_col):
        player = EPlayer.PLAYER_1 if self.whose_turn() else EPlayer.PLAYER_2
        return self.can_en_passant_bool and current_square_col == self.en_passant_previous[1] \
            and abs(current_square_row - self.en_passant_previous[0]) == 1 \
            and self.get_piece(*self.en_passant_previous).get_player() != player

    def previous_piece_en_passant(self):
        return self.en_passant_previous

    # Move a piece
    def move_piece(self, starting_square: tuple[int, int], ending_square: tuple[int, int], is_ai=False):
        moving_piece = self.get_piece(*starting_square)  # The chess piece at the starting square
        current_player = EPlayer.PLAYER_1 if self.whose_turn() else EPlayer.PLAYER_2
        # The current player
        # Is the piece a valid choice?
        valid_piece_choice = moving_piece != EPlayer.EMPTY and moving_piece.is_player(current_player)
        move = None
        if valid_piece_choice:

            valid_moves = moving_piece.get_valid_piece_moves(self)  # The valid moves for the piece

            if ending_square in valid_moves:
                moved_to_piece = self.get_piece(*ending_square)

                # if the piece is king, check if it can castle
                if moving_piece.get_name() == "k" and moved_to_piece == EPlayer.EMPTY:
                    if ending_square[1] == 2 and self.king_can_castle_left(moving_piece.get_player()):
                        move = CastleMove(starting_square, ending_square, self, self._is_check,
                                          (starting_square[0], 0), (starting_square[0], 3))
                    elif ending_square[1] == 6 and self.king_can_castle_right(moving_piece.get_player()):
                        move = CastleMove(starting_square, ending_square, self, self._is_check,
                                          (starting_square[0], 7), (starting_square[0], 5))
                    else:
                        move = ChessMove(starting_square, ending_square, self, self._is_check)

                elif moving_piece.get_name() == "p":
                    # Promoting white pawn
                    if (moving_piece.is_player(EPlayer.PLAYER_1) and ending_square[0] == 7) \
                            or (moving_piece.is_player(EPlayer.PLAYER_2) and ending_square[0] == 0):
                        move = PawnPromotionMove(starting_square, ending_square, self, self._is_check, is_ai)

                    elif abs(ending_square[0] - starting_square[0]) == 2 and ending_square[1] == starting_square[1]:
                        move = TwoSquarePawnMove(starting_square, ending_square, self, self._is_check)

                    # en passant
                    elif self.can_en_passant(*ending_square):
                        move = EnPassantMove(starting_square, ending_square, self, self._is_check)
                    # moving forward by one or taking a piece
                    else:
                        move = ChessMove(starting_square, ending_square, self, self._is_check)
                else:
                    move = ChessMove(starting_square, ending_square, self, self._is_check)
        if bool(move):
            engine_logger.logger.debug("Move made: %s to %s", starting_square, ending_square)
            move.move()

            if moving_piece.get_name() == "r":
                rook_num = (starting_square[0] // 7) + 1
                self.player_stats[moving_piece.get_player()]["can_castle"][rook_num] = False
            self.moves += 1
            self.move_log.append(move)
            self.white_turn = not self.white_turn
            self.player_stats[EPlayer.PLAYER_1]["valid_moves"] = []
            self.player_stats[EPlayer.PLAYER_2]["valid_moves"] = []

    def undo_move(self, is_ai=False):

        if bool(self.move_log):
            undoing_move = self.move_log.pop()
            engine_logger.logger.debug("Undoing move: %s", undoing_move)
            undoing_move.undo()
            self.white_turn = not self.white_turn
            self._all_valid_moves = []
            return undoing_move

        else:
            engine_logger.logger.debug("No moves to undo. Reached the beginning!")
            print("Back to the beginning!")

    # true if white, false if black
    def whose_turn(self):
        return self.white_turn

    '''
    check for immediate check
    - check 8 directions and 8 knight squares
    check for pins
    - whatever blocked from above is a pin
    
     - if immediate check, change check value to true
     - list valid moves to prevent check but not remove pin
     - if there are no valid moves to prevent check, checkmate
    '''

    def check_for_check(self, starting_square: tuple[int, int], player: str):
        # check for immediate check
        checks = []
        # check 8 directions and 8 knight squares
        pins = []
        pins_check = []
        if player is EPlayer.PLAYER_1:
            opponent = EPlayer.PLAYER_2
        else:
            opponent = EPlayer.PLAYER_1

        king_location = self.player_stats[player]["king_location"]

        # check 8 directions and for immediate check and pins (if there is a piece in the way) and
        # pins_check (if there is a piece in the way that is not a king)
        for direction in PieceDirection.KING_DIRECTIONS:
            possible_pin = ()
            square = (king_location[0] + direction[0], king_location[1] + direction[1])
            while self.get_piece(*square) is not None:
                if self.is_valid_piece(*square):
                    piece = self.get_piece(*square)
                    if piece.is_player(opponent):
                        if possible_pin:
                            temp = self.board[possible_pin[0]][possible_pin[1]]
                            self.board[possible_pin[0]][possible_pin[1]] = EPlayer.EMPTY
                            if king_location in piece.get_valid_piece_takes(self):
                                pins.append(possible_pin)
                                pins_check.append(square)
                            self.board[possible_pin[0]][possible_pin[1]] = temp
                        elif king_location in piece.get_valid_piece_takes(self):
                            checks.append(square)
                        break
                    elif piece.is_player(player) and piece.get_name() != 'k':
                        if not possible_pin:
                            possible_pin = square
                        else:
                            break
                square = (square[0] + direction[0], square[1] + direction[1])

        # check for knight checks
        for direction in PieceDirection.KNIGHT_DIRECTIONS:
            square = (king_location[0] + direction[0], king_location[1] + direction[1])
            if self.is_valid_piece(*square):
                piece = self.get_piece(*square)
                if piece.is_player(opponent):
                    if king_location in piece.get_valid_piece_takes(self):
                        checks.append(square)
        if checks:
            self.player_stats[player]["in_check"] = True
        else:
            self.player_stats[player]["in_check"] = False
        return [pins_check, checks, pins]
