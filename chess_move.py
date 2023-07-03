from Piece import Queen, Rook, Bishop, Knight
from enums import EPlayer
from logger import ChessLogger

logger = ChessLogger("moves", "chess_move.log", h="console")


class ChessMove:
    def __init__(self, starting_square, ending_square, game_state, in_check):
        # save locations of the starting and ending squares
        self.starting_square = starting_square
        self.ending_square = ending_square

        # save the piece that was moved and the piece that was removed
        self.moving_piece = game_state.board[starting_square]
        self.removed_piece = game_state.board[ending_square]

        # save the game states
        self.in_check = in_check
        self.game_state = game_state
        self.castling_state = game_state.player_stats[self.moving_piece.get_player()]["can_castle"].copy()
        self.previous_state = self.game_state.can_en_passant_bool
        self.previous_square = self.game_state.en_passant_previous

    def move(self):
        # log the move
        # logger.logger.info(f"Moving {self.moving_piece.__str__()} from {self.starting_square} to {self.ending_square}")
        castle_states = self.game_state.player_stats[self.moving_piece.get_player()]["can_castle"]
        # Change the en passant state to false (as it can only be used on the turn after it is created)
        self.game_state.can_en_passant_bool = False
        # Check if the piece is a king to update its location on the board and to disable castling
        if self.moving_piece.get_name() == "k":
            self.game_state.player_stats[self.moving_piece.get_player()]["king_location"] = self.ending_square
            if castle_states[0]:
                castle_states[0] = False
            # log the king's new location
            # logger.logger.info(f"{self.moving_piece.__str__()} new location: {self.ending_square}")

        if self.moving_piece.get_name() == "r":
            if self.starting_square == (0, 0) and castle_states[1]:
                castle_states[1] = False
            elif self.starting_square == (7, 0) and castle_states[2]:
                castle_states[2] = False

        # Change the piece's position to the ending square
        self.moving_piece.change_pos(self.ending_square)
        if self.removed_piece != EPlayer.EMPTY:
            self.removed_piece.change_pos(self.starting_square)
        self.game_state.board[self.starting_square] = EPlayer.EMPTY
        # update the moving piece's position on the board
        self.game_state.board[self.ending_square] = self.moving_piece

    def undo(self):

        # log the undo
        # logger.logger.info(f"Undo moving {self.moving_piece.__str__()} from {self.starting_square}"
        #                    f" to {self.ending_square}")

        # Revert the piece's position to the ending square
        self.moving_piece.change_pos(self.starting_square)
        if self.removed_piece != EPlayer.EMPTY:
            self.removed_piece.change_pos(self.ending_square)
        self.game_state.board[self.ending_square] = self.removed_piece
        self.game_state.board[self.starting_square] = self.moving_piece

        # Check if the piece is a king to update to its previous location on the board and reset castling state
        if self.moving_piece.get_name() == "k":
            self.game_state.player_stats[self.moving_piece.get_player()]["king_location"] = self.starting_square
            # log the king's previous location
            # logger.logger.info(f"Undo moving {self.moving_piece.__str__()}. previous location: {self.starting_square}")

        # Reset the board to the previous state
        self.game_state.can_en_passant_bool = self.previous_state
        self.game_state.en_passant_previous = self.previous_square
        self.game_state.player_stats[self.moving_piece.get_player()]["can_castle"] = self.castling_state

    def get_starting_square(self):
        return self.starting_square

    def get_ending_square(self):
        return self.ending_square

    def get_moving_piece(self):
        return self.moving_piece


class CastleMove(ChessMove):

    def __init__(self, starting_square, ending_square, game_state, in_check, rook_starting_square, rook_ending_square):
        super().__init__(starting_square, ending_square, game_state, in_check)

        # save the rook's starting and ending squares
        self.rook_starting_square = rook_starting_square
        self.rook_ending_square = rook_ending_square

        # save the rook that was moved
        self.moving_rook = game_state.board[rook_starting_square]

    def update_board(self, starting_square, ending_square, rook_starting_square,
                     rook_ending_square, can_castle):
        # the rook number is 1 if the rook is on the left side of the board, 2 if it is on the right
        rook_num = (self.starting_square[0] // 6) + 1

        # update the castling state
        self.game_state.king_can_castle[self.moving_piece.get_player()][0] = can_castle
        self.game_state.king_can_castle[self.moving_piece.get_player()][rook_num] = can_castle

        # update the king and the rook's location on the board
        self.moving_piece.change_pos(ending_square)
        self.moving_rook.change_pos(rook_ending_square)

        # update the king's location
        self.game_state.king_location[self.moving_piece.get_player()] = self.moving_piece.get_pos()

        # update the board
        self.game_state.board[starting_square] = EPlayer.EMPTY
        self.game_state.board[rook_starting_square] = EPlayer.EMPTY
        self.game_state.board[ending_square] = self.moving_piece
        self.game_state.board[rook_ending_square] = self.moving_rook

    def move(self):
        # log the castling move
        # logger.logger.info(f"Castle move {self.moving_piece.__str__()} "
        #                    f"from {self.starting_square} to {self.ending_square}")

        # disable en passant
        self.game_state.can_en_passant_bool = False

        # update the king and the rook's location on the board
        self.update_board(self.starting_square, self.ending_square,
                          self.rook_starting_square, self.rook_ending_square, False)

    def undo(self, can_castle=True):
        # log the castling undo
        # logger.logger.info(f"Undo castle move {self.moving_piece.__str__()} "
        #                    f"from {self.starting_square} to {self.ending_square}")

        # update the en passant state
        self.game_state.can_en_passant_bool = self.previous_state

        # update the board state
        self.update_board(self.ending_square, self.starting_square,
                          self.rook_ending_square, self.rook_starting_square, can_castle)


class PawnPromotionMove(ChessMove):

    def __init__(self, starting_square, ending_square, game_state, in_check, is_ai):
        super().__init__(starting_square, ending_square, game_state, in_check)
        self.replacement_piece = None
        self.is_ai = is_ai
        self.player = self.moving_piece.get_player()

    def move(self):
        piece_classes = {"r": Rook, "n": Knight, "b": Bishop, "q": Queen}
        if self.is_ai:
            self.moving_piece = Queen("q", *self.ending_square, self.moving_piece.get_player())
        else:
            new_piece_name = ""
            while new_piece_name not in piece_classes:
                new_piece_name = input("Change pawn to (r, n, b, q):\n")
                self.replacement_piece = piece_classes[new_piece_name](new_piece_name,
                                                                       *self.ending_square,
                                                                       self.moving_piece.get_player())
        self.game_state.board[self.starting_square] = EPlayer.EMPTY
        self.game_state.board[self.ending_square] = self.replacement_piece
        # logger.logger.info(f"Promoting pawn to {self.moving_piece.__str__()} "
        #                    f"in square: {self.starting_square}")

    def undo(self):
        # logger.logger.info(f"Undo promote pawn to {self.moving_piece.__str__()} "
        #                    f"in square: {self.starting_square}")
        self.game_state.board[self.starting_square] = self.moving_piece
        self.game_state.board[self.ending_square] = EPlayer.EMPTY


class TwoSquarePawnMove(ChessMove):

    def __init__(self, starting_square, ending_square, game_state, in_check):
        super().__init__(starting_square, ending_square, game_state, in_check)
        self.previous_state = self.game_state.can_en_passant_bool
        self.previous_square = self.game_state.en_passant_previous

    def move(self):
        # logger.logger.info(f"{self.moving_piece.__str__()} moves two squares "
        #                    f"from {self.starting_square} to {self.ending_square}")
        self.moving_piece.change_pos(self.ending_square)
        self.game_state.can_en_passant_bool = True
        self.game_state.en_passant_previous = self.ending_square
        self.game_state.board[self.ending_square] = self.moving_piece
        self.game_state.board[self.starting_square] = EPlayer.EMPTY

    def undo(self):
        # logger.logger.info(f"Undo two square moves for {self.moving_piece.__str__()} "
        #                    f"from {self.starting_square} to {self.ending_square}")
        self.moving_piece.change_pos(self.starting_square)
        self.game_state.can_en_passant_bool = self.previous_state
        self.game_state.en_passant_previous = self.previous_square
        self.game_state.board[self.starting_square] = self.moving_piece
        self.game_state.board[self.ending_square] = EPlayer.EMPTY


class EnPassantMove(ChessMove):

    def __init__(self, starting_square, ending_square, game_state, in_check):
        super().__init__(starting_square, ending_square, game_state, in_check)
        self.add = -1 if self.moving_piece.is_player(EPlayer.PLAYER_1) else 1
        self.removed_piece = self.game_state.board[ending_square[0] + self.add][ending_square[1]]

    def update_board(self, removed_piece):
        self.game_state.board[self.removed_piece.get_pos()] = removed_piece
        self.game_state.board[self.moving_piece.get_pos()] = self.moving_piece

    def move(self):
        # logger.logger.info(f"En Passant Move {self.moving_piece.__str__()} "
        #                    f"from {self.starting_square} to {self.ending_square}")
        self.game_state.can_en_passant_bool = False
        self.game_state.board[self.starting_square] = EPlayer.EMPTY
        self.moving_piece.change_pos(self.ending_square)
        self.update_board(EPlayer.EMPTY)

    def undo(self):
        # logger.logger.info(f"Undo En Passant Move {self.moving_piece.__str__()} "
        #                    f"from {self.ending_square} to {self.starting_square}")
        self.game_state.can_en_passant_bool = True
        self.game_state.board[self.ending_square] = EPlayer.EMPTY
        self.moving_piece.change_pos(self.starting_square)
        self.update_board(self.removed_piece)
