class Player:

    def __init__(self, pieces: list):
        self._pieces = pieces
        self._check = False
        self._checkmate = False
        self._captured_pieces = []
        self._moves = 0
        for piece in pieces:
            if piece.get_name() == "k":
                self._king_location = piece.get_location()
        # if king is not present, then the king is in the starting position
        if not self._king_location:
            raise Exception("King not found")

    def get_color(self):
        return self._color

    def get_pieces(self):
        return self._pieces

    def get_check(self):
        return self._check

    def get_checkmate(self):
        return self._checkmate

    def get_captured_pieces(self):
        return self._captured_pieces

    def get_moves(self):
        return self._moves

    @property
    def set_check(self, check):
        self._check = check

    @property
    def set_checkmate(self, checkmate):
        self._checkmate = checkmate

    @property
    def capture(self, captured_piece):
        self._captured_pieces.append(captured_piece)

    @property
    def release_piece(self, piece):
        self._pieces.pop(piece)

    @property
    def increase_move(self):
        self._moves += 1

    @property
    def decrease_moves(self):
        self._moves -= 1

    @property
    def remove_piece(self, piece):
        self._pieces.pop(piece)

    @property
    def add_piece(self, piece):
        self._pieces.append(piece)

    def get_king_location(self):
        for piece in self._pieces:
            if piece.get_name() == "k":
                return piece.get_location()
        else:
            self._checkmate = True
        return None
