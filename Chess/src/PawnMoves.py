import src.Move as Move


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
        # piece_pinned, pin_direction = self.check_pawn_bishop_knight_pin(
        #     row, col)

        piece_pinned, pin_direction = self.check_pawn_bishop_knight_pin(
            row, col)

        if self.white_to_move:
            move_amount = -1
            start_row = 6
            back_row = 0
            enemy_color = "b"
        else:
            move_amount = 1
            start_row = 1
            back_row = 7
            enemy_color = "w"

        king_row, king_col = self.get_king_location()

        pawn_promotion = False
        if self.board[row + move_amount][col] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                if row + move_amount == back_row:
                    pawn_promotion = True
                moves.append(
                    Move.Move((row, col), (row + move_amount, col), self.board, is_pawn_promotion=pawn_promotion))

                # 2 square pawn advance
                if row == start_row and self.board[row + 2 * move_amount][col] == "--":
                    moves.append(
                        Move.Move((row, col), (row + 2 * move_amount, col), self.board))
        if col - 1 >= 0:  # capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if row + move_amount == back_row:
                    pawn_promotion = True

                if self.board[row + move_amount][col - 1][0] == enemy_color:
                    moves.append(
                        Move.Move((row, col), (row + move_amount, col - 1), self.board, is_pawn_promotion=pawn_promotion))

                if (row + move_amount, col - 1) == self.en_passant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col + 1, col - 1)
                            outer_range = range(col + 1, 8)
                        else:
                            inside_range = range(king_col - 1, col, -1)
                            outer_range = range(col - 2, -1, -1)

                        for c in inside_range:
                            if self.board[row][c] != "--":
                                blocking_piece = True
                        for c in outer_range:
                            square = self.board[row][c]
                            if square[0] == enemy_color and (square[1] in ["R", "Q"]):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True

                    if not attacking_piece or blocking_piece:
                        moves.append(
                            Move.Move((row, col), (row + move_amount, col - 1), self.board, is_en_passant_move=True))

        if col + 1 <= 7:  # capture to the right
            if not piece_pinned or pin_direction == (move_amount, +1):
                if row + move_amount == back_row:
                    pawn_promotion = True

                if self.board[row + move_amount][col + 1][0] == enemy_color:
                    moves.append(
                        Move.Move((row, col), (row + move_amount, col + 1), self.board, is_pawn_promotion=pawn_promotion))

                if (row + move_amount, col + 1) == self.en_passant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col + 1, col)
                            outer_range = range(col + 2, 8)
                        else:
                            inside_range = range(king_col - 1, col + 1, -1)
                            outer_range = range(col - 1, -1, -1)

                        for c in inside_range:
                            if self.board[row][c] != "--":
                                blocking_piece = True
                        for c in outer_range:
                            square = self.board[row][c]
                            if square[0] == enemy_color and (square[1] in ["R", "Q"]):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True

                    if not attacking_piece or blocking_piece:
                        moves.append(
                            Move.Move((row, col), (row + move_amount,  col + 1), self.board, is_en_passant_move=True))
