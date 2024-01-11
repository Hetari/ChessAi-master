import numpy as np


class Move:
    """
        Initializes an instance of the class.

        Parameters:
            start_square (tuple): The starting square coordinates (row, column).
            end_square (tuple): The ending square coordinates (row, column).
            board (np.ndarray): The game board.

        Returns:
            None
        """
    ranks_to_row = {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0,
    }
    row_to_rank = {
        value: key
        for key, value in ranks_to_row.items()
    }

    files_to_cols = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }
    cols_to_files = {
        value: key
        for key, value in files_to_cols.items()
    }

    def __init__(self, start_square: tuple, end_square: tuple, board: np.ndarray) -> None:

        self.start_row = start_square[0]
        self.start_col = start_square[1]

        self.end_row = end_square[0]
        self.end_col = end_square[1]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_chess_notation(self) -> str:
        """
        Get the chess notation for the start and end positions of the chess piece.

        Returns:
            str: The chess notation for the start and end positions.
        """
        # for example it will return c7e5
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row: int, col: int) -> tuple[str, int]:
        """
        Get the rank and file of a given position.

        Args:
            row (int): The row of the position.
            col (int): The column of the position.

        Returns:
            Tuple[str, int]: The rank and file of the position.
        """
        return self.cols_to_files[col], self.ranks_to_row[str(row)]
