import numpy as np


class Move:
    """
        Initializes an instance of the class.

        Args:
            start_square (tuple): The starting square coordinates (row, column).
            end_square (tuple): The ending square coordinates (row, column).
            board (np.ndarray): The game board.

        Returns:
            None
        """
    ranks_to_rows = {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0
    }
    row_to_ranks = {
        value: key
        for key, value in ranks_to_rows.items()
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
        # From
        self.start_row = start_square[0]
        self.start_col = start_square[1]

        # To:
        self.end_row = end_square[0]
        self.end_col = end_square[1]

        # What is moving?
        self.piece_moved = board[self.start_row][self.start_col]

        # The moving piece eat this:
        self.piece_captured = board[self.end_row][self.end_col]

        # Id
        self.move_id = self.start_row * 1000 + self.start_col * \
            100 + self.end_row * 10 + self.end_col

    def get_chess_notation(self) -> str:
        """
        Get the chess notation for the start and end positions of the chess piece.

        Returns:
            str: The chess notation for the start and end positions.
        """
        # for example it will return c7e5
        # return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row: int, col: int) -> str:
        """
        Get the rank and file of a given position.

        Args:
            row (int): The row of the position.
            col (int): The column of the position.

        Returns:
            Tuple[str, int]: The rank and file of the position.
        """
        return self.cols_to_files[col] + self.row_to_ranks[row]

    def __eq__(self, other: object) -> bool:
        return self.move_id == other.move_id if isinstance(other, Move) else False
