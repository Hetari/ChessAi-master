import Move


class Bishop:
    def bishop_moves(self, row, col, moves):
        piece_pinned, pin_direction = self.check_pawn_bishop_knight_pin(
            row, col)

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))

        # get the enemy color
        enemy_color = "b" if self.white_to_move else "w"

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if not self.is_valid_position(end_row, end_col):
                    break

                if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                    end_piece = self.board[end_row][end_col]

                    # empty space is valid
                    if end_piece == "--":
                        moves.append(
                            Move.Move((row, col), (end_row, end_col), self.board))

                    # capture enemy piece
                    elif end_piece[0] == enemy_color:
                        moves.append(
                            Move.Move((row, col), (end_row, end_col), self.board))
                        break

                    # friendly piece
                    else:
                        break
