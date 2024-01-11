import numpy as np
import Move


class GameState():
    def __init__(self) -> None:
        # board is 8x8 2d list, each element of list has 2 characters
        # 0 represents an empty space
        # 1 represents a black rook
        # 2 represents a black knight
        # 3 represents a black bishop
        # 4 represents a black queen
        # 5 represents a black king
        # 6 represents a black pawn
        # 7 represents a white rook
        # 8 represents a white knight
        # 9 represents a white bishop
        # 10 represents a white queen
        # 11 represents a white king
        # 12 represents a white pawn
        self.board = np.array([
            [7, 8, 9, 10, 11, 9, 8, 7],
            [12, 12, 12, 12, 12, 12, 12, 12],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [1, 2, 3, 4, 5, 3, 2, 1]
        ], dtype=np.int8)

        self.white_to_move = True
        self.move_log = []

    def make_move(self, move: Move) -> None:
        # make the piece location empty
        self.board[move.start_row][move.start_col] = 0

        # move the piece to the ending location
        self.board[move.end_row][move.end_col] = move.piece_moved

        self.move_log.append(move)
        self.white_to_move = not self.white_to_move


class Color:
    def __init__(self, light, dark):
        self.light = light
        self.dark = dark


class Theme:
    def __init__(self, light_bg, dark_bg,
                 light_trace, dark_trace,
                 light_moves, dark_moves):
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)


class Config():
    def __init__(self) -> None:
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247,
                      116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234,
                      100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187,
                     227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143),
                     (82, 102, 128), '#C86464', '#C84646')

        self.themes = [green, brown, blue, gray]
