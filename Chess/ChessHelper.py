class Helper:
    def update_king_location(self, king: str, row: int, col: int) -> None:
        """
        Updates the location of the king in the board.

        Args:
            king (str): The name of the king ('wK' or 'bK').
            row (int): The row of the king's new location.
            col (int): The column of the king's new location.

        Returns:
            None
        """
        if king == "wK":
            self.white_king_location = (row, col)
        elif king == "bK":
            self.black_king_location = (row, col)

    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if the given row and column are valid positions on the board.

        Args:
        row (int): The row index.
        col (int): The column index.

        Returns:
        bool: True if the position is valid, False otherwise.
        """
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])

    # @staticmethod
    def get_king_location(self) -> tuple[int, int]:
        """
        Returns the current location of the king based on whose turn it is.

        Returns:
            Tuple[int, int]: The row and column of the king.
        """
        return self.white_king_location if self.white_to_move else self.black_king_location

    def check_pawn_bishop_knight_pin(self, pins, row, col):
        """
        Check if a piece is pinned by any pins at the specified row and column.

        Args:
        pins: List of pins on the board.
        row: Row of the piece.
        col: Column of the piece.

        Returns:
        Tuple containing a boolean representing if the piece is pinned and the direction of the pin if it is pinned.
        """

        piece_pinned = False
        pin_direction = ()

        for i in range(len(pins) - 1, -1, -1):
            # Check if the pin is at the specified row and column
            if pins[i][0] == row and pins[i][1] == col:
                # Remove the pin from the list, because it is pinned and we can't move it
                piece_pinned = True
                pin_direction = (pins[i][2], pins[i][3])
                pins.remove(pins[i])
                break
        return piece_pinned, pin_direction
