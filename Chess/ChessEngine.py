import numpy as np
import Move
import pygame as p


class GameState():
    """
    The GameState class keeps track of the chess board, the current player's turn, and the move history. It provides methods to make moves, undo moves, and get all possible moves for the current state of the game.

    Attributes:
        board: A 2D list representing the chess board.
        move_functions: A dictionary mapping piece types to their corresponding move functions.
        white_to_move: A boolean indicating whether it is currently white's turn to move.
        move_log: A list of Move objects representing the move history.

    Methods:
        make_move: Makes a move on the chess board.
        undo_move: Undoes the last move made in the game.
        get_valid_moves: Returns a list of all valid moves for the current state of the game.
        get_all_possible_moves: Returns a list of all possible moves for the current state of the game.
        get_pawn_moves: Generates valid moves for a pawn at a given position.
    """

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
        self.board: np.ndarray = np.array([
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
        self.move_functions: dict[int, callable] = {
            6: self.get_pawn_moves,
            12: self.get_pawn_moves
        }

        self.white_to_move: bool = True
        self.move_log: list[Move.Move] = []

    def make_move(self, move: Move) -> None:
        """
        Makes a move on the chess board.

        This method updates the chess board, the current player's turn, and the move history based on the given move.

        Args:
            move (Move): The move to be made.

        Returns:
            None
        """
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
        Undoes the last move made in the game.
        This method removes the last move from the move log and updates the board accordingly. If there are no moves in the move log, the method returns without making any changes to the game state.

        Args:
            None

        Returns:
            None
        """
        if len(self.move_log) == 0:
            return
        move: Move.Move = self.move_log.pop()
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured
        self.white_to_move = not self.white_to_move

    def get_valid_moves(self) -> list[Move.Move]:
        """
        Returns a list of all valid moves for the current state of the game.

        This method calls the get_all_possible_moves method to get all possible moves and filters out the invalid moves.

        Args:
            None

        Returns:
            list[Move]: A list of all valid moves.
        """
        return self.get_all_possible_moves()

    def get_all_possible_moves(self) -> list[Move.Move]:
        """
        Get all possible and valid moves for the current state of the game.

        Returns:
            list[Move]: A list of all possible and valid moves.
        """
        moves: list[Move.Move] = []
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

    def __append_pawn_move(self, start: tuple[int], end: tuple[int], moves: list[Move.Move]):
        """
        Append a pawn move to the list of moves.

        Args:
            start (tuple[int]): The starting position of the pawn move.
            end (tuple[int]): The ending position of the pawn move.
            moves (list[Move.Move]): The list of moves to append the pawn move to.

        Returns:
            None
        """
        if self.__is_valid_position(end[0], end[1]):
            moves.append(Move.Move(start, end, self.board))

    def __append_pawn_capture(self, start: tuple[int], end: tuple[int], moves: list[Move.Move]):
        """
        Appends a pawn capture move to the list of moves.

        Parameters:
            start (tuple[int]): The starting position of the pawn.
            end (tuple[int]): The ending position of the pawn after the capture.
            moves (list[Move.Move]): The list of moves to append the capture move to.

        Returns:
            None
        """
        # Check if the ending position is a valid position on the board, then:
        # Check if the captured piece is an opponent's piece, then:
        # Create a new move object and append it to the list of moves
        if self.__is_valid_position(end[0], end[1]) and ((self.white_to_move and self.board[end[0]][end[1]] in range(1, 7)) or (not self.white_to_move and self.board[end[0]][end[1]] in range(7, 13))):
            moves.append(Move.Move(start, end, self.board))

    def __is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if the given row and column are valid positions on the board.

        Args:
        row (int): The row index.
        col (int): The column index.

        Returns:
        bool: True if the position is valid, False otherwise.
        """
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])


class Color:
    """
    class Color:
    Represents a color with a light and dark shade.

    Args:
        light: The light shade of the color.
        dark: The dark shade of the color.
    """

    def __init__(self, light: tuple[int, int, int], dark: tuple[int, int, int]):
        self.light: tuple[int, int, int] = light
        self.dark: tuple[int, int, int] = dark


class Theme:
    """
    Represents a theme for a chess game.

    Args:
        light_bg: The light background color.
        dark_bg: The dark background color.
        light_trace: The light color for trace lines.
        dark_trace: The dark color for trace lines.
        light_moves: The light color for move indicators.
        dark_moves: The dark color for move indicators.
    """

    def __init__(self, light_bg: int, dark_bg: int,
                 light_trace: int, dark_trace: int,
                 light_moves: int, dark_moves: int):
        self.bg: Color = Color(light_bg, dark_bg)
        self.trace: Color = Color(light_trace, dark_trace)
        self.moves: Color = Color(light_moves, dark_moves)


class Config():
    """
    Represents the configuration for a chess game.

    Attributes:
        themes: A list of available themes.
        idx: The index of the current theme.
        theme: The current theme.

    Methods:
        change_theme: Changes the current theme to the next one.
    """

    def __init__(self):
        self.themes: list[Theme] = []
        self._add_themes()
        self.idx: int = 0
        self.theme: Theme = self.themes[self.idx]

    def change_theme(self):
        """
        Changes the current theme to the next one.
        """
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        """
        Adds predefined themes to the list of available themes.
        """
        green: Theme = Theme(
            (234, 235, 200),
            (119, 154, 88),
            (244, 247, 116),
            (172, 195, 51),
            '#C86464',
            '#C84646',
        )

        brown: Theme = Theme(
            (235, 209, 166),
            (165, 117, 80),
            (245, 234, 100),
            (209, 185, 59),
            '#C86464',
            '#C84646',
        )
        blue: Theme = Theme(
            (229, 228, 200),
            (60, 95, 135),
            (123, 187, 227),
            (43, 119, 191),
            '#C86464',
            '#C84646',
        )

        gray: Theme = Theme(
            (120, 119, 118),
            (86, 85, 84),
            (99, 126, 143),
            (82, 102, 128),
            '#C86464',
            '#C84646',
        )

        self.themes = [green, brown, blue, gray]
