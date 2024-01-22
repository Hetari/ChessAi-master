import numpy as np
import Move
import pygame as p


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
            [1, 2, 3, 4, 5, 3, 2, 1],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0],
            [12, 12, 12, 12, 12, 12, 12, 12],
            [7, 8, 9, 10, 11, 9, 8, 7],
        ], dtype=np.int8)

        # Get the possible moves for each piece
        self.move_functions = {
            6: self.get_pawn_moves,
            12: self.get_pawn_moves
        }

        self.white_to_move = True
        self.move_log = []

    def make_move(self, move: Move) -> None:
        # Make the piece location empty
        self.board[move.start_row][move.start_col] = 0

        # Move the piece to the new location
        self.board[move.end_row][move.end_col] = move.piece_moved

        # Add the new move to the log
        self.move_log.append(move)

        # Toggle the order of moves
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """
        Undo the last move made in the game.

        This function removes the last move from the move log and updates the board accordingly. If there are no moves in the move log, the function returns without making any changes to the game state.

        Parameters:
            None

        Returns:
            None
        """
        if len(self.move_log) == 0:
            return
        move = self.move_log.pop()
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        """
        Get all possible and valid moves for the current state of the game.

        Returns:
            list[Move]: A list of all possible and valid moves.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.board[row][col]

                # check the turn of the piece is  black from 1 to 6, or white from 7 to 12

                # piece in range(7, 13) and
                if piece in range(13):
                    self.move_functions.get(
                        piece, lambda *_: None)(row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:
            if self.board[row - 1][col] == 0:
                moves.append(Move.Move(
                    (row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == 0:
                    moves.append(
                        Move.Move((row, col), (row - 2, col), self.board))
            if col >= 1 and self.board[row - 1][col - 1] < len(self.board[row]):
                moves.append(Move.Move(
                    (row, col), (row - 1, col - 1), self.board))

            if col + 1 < len(self.board[row]) and self.board[row - 1][col + 1] < len(self.board[row]):
                moves.append(Move.Move(
                    (row, col), (row - 1, col + 1), self.board))

        elif self.board[row + 1][col] == 0:
            moves.append(Move.Move((row, col), (row + 1, col), self.board))
            if row == 1 and self.board[row + 2][col] == 0:
                moves.append(
                    Move.Move((row, col), (row + 2, col), self.board))


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
