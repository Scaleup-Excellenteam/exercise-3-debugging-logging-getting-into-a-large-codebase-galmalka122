class EPlayer:
    PLAYER_1 = 'white'
    PLAYER_2 = 'black'
    EMPTY = -9
    PIECES = ['white_r', 'white_n', 'white_b', 'white_q', 'white_k', 'white_p',
              'black_r', 'black_n', 'black_b', 'black_q', 'black_k', 'black_p']


class PieceDirection:
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, 1)
    DOWN_LEFT = (1, -1)
    DOWN_RIGHT = (1, 1)

    KNIGHT_DIRECTIONS = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                         (1, 2), (1, -2), (-1, 2), (-1, -2)]
    BISHOP_DIRECTIONS = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
    ROOK_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
    QUEEN_DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
    KING_DIRECTIONS = QUEEN_DIRECTIONS
