import src.Move as Move


class Rock():
    def rock_moves(self, row, col, moves):
        piece_pinned, pin_direction = self.check_rock_pin(self.pins, row, col)

        # Define directions for possible rook moves
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.white_to_move else "w"

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if not self.is_valid_position(end_row, end_col):
                    break

                # Check if the rook is not pinned, or if the move is in the direction of the pin, or if the move is in the opposite direction of the pin
                if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                    end_piece = self.board[end_row][end_col]

                    # empty space is valid
                    if end_piece == "--":
                        moves.append(
                            Move.Move((row, col), (end_row, end_col), self.board))

                    elif end_piece[0] == enemy_color:  # capture enemy piece
                        moves.append(
                            Move.Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break

    def check_rock_pin(self, pins, row, col):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(pins) - 1, -1, -1):
            if pins[i][0] == row and pins[i][1] == col:
                # can't remove queen from pin on rook moves, only remove it on bishop moves
                piece_pinned = True
                pin_direction = (pins[i][2], pins[i][3])
                if self.board[row][col][1] != "Q":
                    pins.remove(pins[i])
                break
        return piece_pinned, pin_direction
