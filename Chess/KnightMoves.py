import Move


class Knight:
    def knight_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Generates possible moves for a knight at a given position.

        Args:
            row (int): The row of the knight.
            col (int): The column of the knight.
            moves (list[Move]): The list of possible moves to be updated.

        Returns:
            None
        """
        piece_pinned, _ = self.check_pawn_bishop_knight_pin(row, col)

        # up/left up/right right/up right/down down/left down/right left/up left/down
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2),
                        (2, -1), (2, 1), (-1, -2), (1, -2))
        ally_color = "w" if self.white_to_move else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if self.is_valid_position(end_row, end_col):
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    # so it's either enemy piece or empty equare
                    if end_piece[0] != ally_color:
                        moves.append(
                            Move.Move((row, col), (end_row, end_col), self.board))
