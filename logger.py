import logging
import os.path
import colorlog

from enums import EPlayer


class ChessLogger:

    def __init__(self, name, file, level=logging.DEBUG, h="file"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = None
        formatter = None
        path = os.path.join("logs", file)
        # create a file handler
        if h == "file":
            handler = logging.FileHandler(path)
            handler.setLevel(level)
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

        elif h == "console":
            handler = logging.StreamHandler()
            handler.setLevel(level)
            formatter = colorlog.ColoredFormatter(
                "%(log_color)s%(name)s - %(message)s%(reset)s",
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white'
                }
            )
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def log_board(self, board):
        """
Logs the board to the log file
        :param board: The board to log
        :return: None
        """
        board_string = ""
        for row in board:
            board_string += "---------------------------------\n"
            for col in row:
                if col == -9:
                    board_string += "|   "
                elif col.get_player() == EPlayer.PLAYER_1:
                    board_string += "| " + col.get_name().upper() + " "
                else:
                    board_string += "| " + col.get_name() + " "
            board_string += "|\n"
        board_string += "---------------------------------\n"
        self.logger.debug(board_string)
