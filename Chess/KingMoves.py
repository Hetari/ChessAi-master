import Move


class King:

    def king_moves(self, row, col, moves):
        ally_color: str = "w" if self.white_to_move else "b"
        row_moves: tuple[int] = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves: tuple[int] = (-1, 0, 1, -1, 1, -1, 0, 1)

        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]

            if self.is_valid_position(end_row, end_col):
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    self.update_king_location(
                        f"{ally_color}K", end_row, end_col)

                    in_check, pins, checks = self.check_pins_and_checks()

                    if not in_check:
                        moves.append(
                            Move.Move((row, col), (end_row, end_col), self.board))

                    # place king back on original location
                    self.update_king_location(
                        f"{ally_color}K", end_row, end_col)
