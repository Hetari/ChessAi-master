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
            [0, 0, 0, 0, 0, 0, 0, 0],
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
        self.white_to_move = not self.white_to_move

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

                if piece in range(13):
                    self.move_functions.get(
                        piece, lambda *_: None)(row, col, moves)
        return moves

    def get_pawn_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Generate valid moves for a pawn at a given position.

        Args:
        - row: int, the row of the pawn
        - col: int, the column of the pawn
        - moves: list[Move], list of valid moves

        Returns:
        - None
        """
        if self.__is_valid_position(row, col) and self.white_to_move:
            # Check for empty square in front of the pawn
            if self.__is_valid_position(row + 1, col) and self.board[row - 1][col] == 0:
                self.__append_pawn_move((row, col), (row - 1, col), moves)
                # Check for double-step move from starting row if is in its place
                if row == 6 and self.board[row - 2][col] == 0:
                    self.__append_pawn_move((row, col), (row - 2, col), moves)

            # Check for capturing moves, left and right
            self.__append_pawn_capture((row, col), (row - 1, col - 1), moves)
            self.__append_pawn_capture((row, col), (row - 1, col + 1), moves)

        elif self.__is_valid_position(row, col) and not self.white_to_move:
            if self.__is_valid_position(row + 1, col) and self.board[row + 1][col] == 0:
                self.__append_pawn_move((row, col), (row + 1, col), moves)
                if row == 1 and self.board[row + 2][col] == 0:
                    self.__append_pawn_move((row, col), (row + 2, col), moves)

            self.__append_pawn_capture((row, col), (row + 1, col - 1), moves)
            self.__append_pawn_capture((row, col), (row + 1, col + 1), moves)

    def __append_pawn_move(self, start, end, moves):
        if self.__is_valid_position(end[0], end[1]):
            moves.append(Move.Move(start, end, self.board))

    def __append_pawn_capture(self, start, end, moves):
        if self.__is_valid_position(end[0], end[1]) and ((self.white_to_move and self.board[end[0]][end[1]] in range(1, 7)) or (not self.white_to_move and self.board[end[0]][end[1]] in range(7, 13))):
            moves.append(Move.Move(start, end, self.board))

    def __is_valid_position(self, row, col):
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])


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
