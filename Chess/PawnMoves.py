import Move


class Pawn():
    def pawn_moves(self, row, col, moves):
        """
        Generates valid moves for a pawn piece on the chessboard.

        Args:
            pins (list): List of pinned pieces on the board.
            row (int): The row on the chessboard where the pawn is located.
            col (int): The column on the chessboard where the pawn is located.
            moves (list): List to store the valid moves for the pawn.

        Returns:
            None
        """
        # Check if the pawn is pinned and get the pin direction
        piece_pinned, pin_direction = self.check_pawn_bishop_knight_pin(
            row, col)

        if self.white_to_move:
            if self.is_valid_position(row - 1, col) and self.board[row - 1][col] == "--":
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(
                        Move.Move((row, col), (row - 1, col), self.board))
                    # Double move for first move
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(
                            Move.Move((row, col), (row - 2, col), self.board))

            # Check for capturing moves to the left and add them to the list
            if col - 1 >= 0:
                if self.is_valid_position(row - 1, col - 1) and self.board[row - 1][col - 1][0] == "b":
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(
                            Move.Move((row, col), (row - 1, col - 1), self.board))

            # Check for capturing moves to the right and add them to the list
            if col + 1 <= 7:
                if self.is_valid_position(row - 1, col + 1) and self.board[row - 1][col + 1][0] == "b":
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(
                            Move.Move((row, col), (row - 1, col + 1), self.board))

        else:
            if self.is_valid_position(row + 1, col) and self.board[row + 1][col] == "--":
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(
                        Move.Move((row, col), (row + 1, col), self.board))
                    # Moving two squares forward if in starting position
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(
                            Move.Move((row, col), (row + 2, col), self.board))

            # Capturing diagonally to the left
            if col - 1 >= 0:
                if self.is_valid_position(row + 1, col - 1) and self.board[row + 1][col - 1][0] == "w":
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(
                            Move.Move((row, col), (row + 1, col - 1), self.board))

            # Capturing diagonally to the right
            if col + 1 <= 7:
                if self.is_valid_position(row + 1, col + 1) and self.board[row + 1][col + 1][0] == "w":
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(
                            Move.Move((row, col), (row + 1, col + 1), self.board))
