class Move:
    """
        Initializes an instance of the class.

        Args:
            start_square (tuple): The starting square coordinates (row, column).
            end_square (tuple): The ending square coordinates (row, column).
            board (list[str]): The game board.

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

    def __init__(self, start_square: tuple, end_square: tuple, board: list[str], is_en_passant_move=False, is_pawn_promotion=False, is_castle_move=False) -> None:
        self.start_row: int = start_square[0]
        self.start_col: int = start_square[1]
        self.end_row: int = end_square[0]
        self.end_col: int = end_square[1]
        self.piece_moved: str = board[self.start_row][self.start_col]
        self.piece_captured: str = board[self.end_row][self.end_col]

        # self.is_pawn_promotion: bool = (self.piece_moved == "wp" and self.end_row == 0) or (
        #     self.piece_moved == "bp" and self.end_row == 7)
        self.is_pawn_promotion: bool = is_pawn_promotion
        self.is_en_passant_move: bool = is_en_passant_move
        if self.is_en_passant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"

        # is castle move
        self.is_castle_move: bool = is_castle_move
        # Id
        # The \ is not an operation, it is allow me to write the rest of code in a new line
        self.move_id: int = self.start_row * 1000 + self.start_col * \
            100 + self.end_row * 10 + self.end_col

    def get_chess_notation(self) -> str:
        """
        Get the chess notation for the start and end positions of the chess piece.

        Returns:
            str: The chess notation for the start and end positions.
        """
        # for example it will return c7e5
        # return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
        name = self.convert_letters_to_words(self.piece_moved[1])
        color = "White" if self.piece_moved[0] == "w" else "Black"
        _from = self.get_rank_file(self.start_row, self.start_col)
        to = self.get_rank_file(self.end_row, self.end_col)
        return f"{color} {name} -> {_from} {to}"

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

    def convert_letters_to_words(self, letter):
        letter_to_word = {
            "b": "bishop",
            "k": "king",
            "q": "queen",
            "p": "pawn",
            "n": "knight",
            "r": "rook",
            "none": "none"}
        return letter_to_word[letter.lower()]

    def __eq__(self, other: object) -> bool:
        return self.move_id == other.move_id if isinstance(other, Move) else False

    def __json__(self):
        return {
            "start_row": self.start_row,
            "start_col": self.start_col,
            "end_row": self.end_row,
            "end_col": self.end_col,
            "piece_moved": self.piece_moved,
            "piece_captured": self.piece_captured,
            "is_pawn_promotion": self.is_pawn_promotion,
            "is_en_passant_move": self.is_en_passant_move,
            "is_castle_move": self.is_castle_move,
            "move_id": self.move_id
        }
