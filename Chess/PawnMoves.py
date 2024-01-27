import Move


class Pawn:
    @staticmethod
    def pawn_moves(self, pins, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(pins) - 1, -1, -1):
            if pins[i][0] == row and pins[i][1] == col:
                piece_pinned = True
                pin_direction = (pins[i][2], pins[i][3])
                pins.remove(pins[i])
                break

        if self.white_to_move:  # white pawn moves
            if self.board[row - 1][col] == "--":  # 1 square pawn advance
                if not piece_pinned or pin_direction == (-1, 0):
                    # (start square, end square, board)
                    moves.append(
                        Move.Move((row, col), (row - 1, col), self.board))
                    # 2 square pawn advance
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(
                            Move.Move((row, col), (row - 2, col), self.board))

            if (
                col - 1 >= 0
            ):  # capturing to the left - impossible if a pawn is standing in a far left column
                if self.board[row - 1][col - 1][0] == "b":  # enemy piece to capture
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(
                            Move.Move(
                                (row, col), (row - 1, col - 1), self.board)
                        )

            if col + 1 <= 7:  # capturing to the right - analogical
                if self.board[row - 1][col + 1][0] == "b":  # enemy piece to capture
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(
                            Move.Move(
                                (row, col), (row - 1, col + 1), self.board)
                        )

        else:  # black pawn moves
            if self.board[row + 1][col] == "--":  # 1 suare pawn advance
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(
                        Move.Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(
                            Move.Move((row, col), (row + 2, col), self.board))

            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == "w":
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(
                            Move.Move(
                                (row, col), (row + 1, col - 1), self.board)
                        )

            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == "w":
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(
                            Move.Move(
                                (row, col), (row + 1, col + 1), self.board)
                        )
