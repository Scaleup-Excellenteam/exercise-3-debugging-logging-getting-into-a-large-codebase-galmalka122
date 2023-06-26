#
# The Chess piece classes
#
# TODO: add checking if check after moving suggested move later

# General chess piece
from enums import Player


def is_valid_square(row, col):
    return (0 <= row < 8) and (0 <= col < 8)


def is_peaceful_move(game_state, square):
    piece = game_state.get_piece(*square)
    return piece and piece is Player.EMPTY


class Piece:
    # Initialize the piece
    def __init__(self, name, row_number, col_number, player):
        self._name = name
        self.row_number = row_number
        self.col_number = col_number
        self._player = player
        self._directions = []
        self._piece_takes = []
        self._peaceful_moves = []

    def add_step(self, direction: tuple):
        return self.row_number + direction[0], self.col_number + direction[1]

    def get_pos(self):
        return self.row_number, self.col_number

    # Get the x value
    def get_row_number(self):
        return self.row_number

    # Get the y value
    def get_col_number(self):
        return self.col_number

    # Get the name
    def get_name(self):
        return self._name

    def get_player(self):
        return self._player

    def is_player(self, player_checked):
        return self.get_player() == player_checked

    def can_move(self, board, starting_square):
        pass

    def can_take(self, is_check):
        pass

    def change_row_number(self, new_row_number):
        self.row_number = new_row_number

    def change_col_number(self, new_col_number):
        self.col_number = new_col_number

    def get_valid_peaceful_moves(self, game_state):
        return self._peaceful_moves

    def get_valid_piece_takes(self, game_state):
        return self._piece_takes

    # Get moves
    def get_valid_piece_moves(self, board):
        pass

    def is_piece_take_move(self, game_state, square):
        return game_state.is_valid_piece(*square) and \
                not game_state.get_piece(*square).is_player(self.get_player())


class SingleStepPiece(Piece):
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)

    def get_valid_piece_moves(self, game_state):
        self._piece_takes.clear()
        self._peaceful_moves.clear()
        for direction in self._directions:
            square = self.add_step(direction)
            if is_peaceful_move(game_state, square):
                self._peaceful_moves.append(square)
            elif self.is_piece_take_move(game_state, square):
                self._piece_takes.append(square)
        return self._peaceful_moves + self._piece_takes


class MultiStepPiece(Piece):
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)

    def get_valid_piece_moves(self, game_state):
        self._piece_takes.clear()
        self._peaceful_moves.clear()
        for direction in self._directions:
            square = self.add_step(direction)
            while is_valid_square(*square):
                if is_peaceful_move(game_state, square):
                    self._peaceful_moves.append(square)
                    square = tuple(a + b for a, b in zip(square, direction))
                else:
                    if self.is_piece_take_move(game_state, square):
                        self._piece_takes.append(square)
                    break
        return self._peaceful_moves + self._piece_takes


# Rook (R)
class Rook(MultiStepPiece):
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        self._directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.has_moved = False

    def __str__(self):
        return "Rook"


# Knight (N)
class Knight(SingleStepPiece):

    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        self._directions = [(-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2), (2, -1), (2, 1)]

    def __str__(self):
        return "Knight"


# Bishop
class Bishop(MultiStepPiece):
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        self._directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __str__(self):
        return "Bishop"


# Pawn
class Pawn(SingleStepPiece):

    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        if self._player == Player.PLAYER_1:
            self._directions = [(1, 0)]
            self._piece_take_directions = [(1, 1), (1, -1)]
            self.first_row = 1
            self.first_step_move = (2, 0)
        else:
            self._directions = [(-1, 0)]
            self._piece_take_directions = [(-1, 1), (-1, -1)]
            self.first_row = 6
            self.first_step_move = (-2, 0)

    def __str__(self):
        return "Pawn"

    def get_valid_piece_moves(self, game_state):
        self._piece_takes.clear()
        self._peaceful_moves.clear()
        for direction in self._directions:
            square = self.add_step(direction)
            if is_peaceful_move(game_state, square):
                self._peaceful_moves.append(square)
        for direction in self._piece_take_directions:
            square = self.add_step(direction)
            if self.is_piece_take_move(game_state, square):
                self._piece_takes.append(square)
        if self.get_row_number() == self.first_row and len(self._peaceful_moves) == 1:
            square = self.add_step(self.first_step_move)
            if is_peaceful_move(game_state, square):
                self._peaceful_moves.append(square)
        return self._peaceful_moves + self._piece_takes


# Queen
class Queen(MultiStepPiece):
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        self._directions = [(1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]

    def __str__(self):
        return "Queen"


# King
class King(SingleStepPiece):

    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        self._directions = [(1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        if self.is_player(Player.PLAYER_1):
            self._castle_directions = [(0, 1), (0, 5)]
        else:
            self._castle_directions = [(7, 1), (7, 5)]

    def __str__(self):
        return "King"

    def get_valid_piece_moves(self, game_state):
        super().get_valid_piece_moves(game_state)
        if game_state.king_can_castle_left(self.get_player()):
            self._piece_takes.append(self._castle_directions[0])
        elif game_state.king_can_castle_right(self.get_player()):
            self._peaceful_moves.append(self._castle_directions[1])

        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)
