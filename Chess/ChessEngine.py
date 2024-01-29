import Move
import PawnMoves
import RockMoves
import KnightMoves
import BishopMoves
import KingMoves
import ChessHelper


class GameState(ChessHelper.Helper,
                PawnMoves.Pawn,
                RockMoves.Rock,
                KnightMoves.Knight,
                BishopMoves.Bishop,
                KingMoves.King,
                ):
    def __init__(self) -> None:
        # board is 8x8 2d list, each element of list has 2 characters
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        # Get the possible moves for each piece
        self.move_functions: dict[int, callable] = {
            "R": self.get_rock_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves,
            "p": self.get_pawn_moves,
        }

        self.white_to_move: bool = True
        self.move_log: list[Move.Move] = []

        # Tracking the king location
        self.white_king_location: tuple[int] = (7, 4)
        self.black_king_location: tuple[int] = (0, 4)

        # Tracking the pins, checks, and checkmate
        self.check_mate: bool = False
        self.stale_mate: bool = False
        self.in_check: bool = False
        self.pins: list = []
        self.checks: list = []

        # coordinates for the square where en passant capture is possible
        self.en_passant_possible: tuple = ()

    def make_move(self, move: Move.Move) -> None:
        """
        Makes a move on the chess board.

        This method updates the chess board, the current player's turn, and the move history based on the given move.

        Args:
            move (Move): The move to be made.

        Returns:
            None
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        # Update the king location, if the move.piece_moved is king
        self.update_king_location(
            move.piece_moved, move.end_row, move.end_col)

        # if pawn moves twice, next move can capture en passant
        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:
            self.en_passant_possible = (
                (move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.en_passant_possible = ()

        # if en passant move, must update the board to capture the pawn
        if move.is_en_passant_move:
            print(f"is_en_passant_move {move.is_en_passant_move}")
            self.board[move.start_row][move.end_col] = "--"

        # if pawn promotion, change piece
        if move.is_pawn_promotion:
            # TODO ask for a piece in UI (Q, R, B, or N)
            promoted_piece: str = input("Promote to Q, R, B, or N:").upper()
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + \
                promoted_piece

    def undo_move(self):
        """
        Undoes the last move made in the game.
        This method removes the last move from the move log and updates the board accordingly. If there are no moves in the move log, the method returns without making any changes to the game state.

        Args:
            None

        Returns:
            None
        """
        if len(self.move_log) == 0:
            return

        move = self.move_log.pop()
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured
        self.white_to_move = not self.white_to_move

        # update the king's position if needed
        self.update_king_location(
            move.piece_moved, move.end_row, move.end_col)

        # undo the en passant move, it is different
        if move.is_en_passant_move:
            # leave landing square blank
            self.board[move.end_row][move.end_col] = "--"
            self.board[move.start_row][move.end_col] = move.piece_captured
            self.en_passant_possible = (move.end_row, move.end_col)

        # undo a 2 square pawn advance should make en_passant_possible = () again
        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:
            self.en_passant_possible = ()

        # self.check_mate = False
        # self.stale_mate = False

    def get_valid_moves(self) -> list[Move.Move]:
        """
        Returns a list of all valid moves for the current state of the game.

        This method calls the get_all_possible_moves method to get all possible moves and filters out the invalid moves.

        Args:
            None+

        Returns:
            list[Move]: A list of all valid moves.
        """
        moves: list[Move.Move] = []

        self.in_check, self.pins, self.checks = self.check_pins_and_checks()

        # get the king location depending on whose turn it is
        king_row, king_col = self.get_king_location()

        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                # to block check you must move a piece into one of the squares between the enemy piece and the king
                check: tuple[int] = self.checks[0]
                valid_squares = []
                self.block_check_valid_squares(
                    check, king_row, king_col)

                self.filter_moves_to_block_check(moves, valid_squares)
            else:
                # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:
            # not in check - all moves are fine
            moves = self.get_all_possible_moves()

        # if len(moves) == 0:
        #     if self.in_check_function():
        #         self.check_mate = True
        #     else:
        #         # TODO stalemate on repeated moves
        #         self.stale_mate = True
        # else:
        #     self.check_mate = False
        #     self.stale_mate = False

        return moves

    # def in_check_function(self):
    #     '''
    #     Determine if a current player is in check
    #     '''
    #     if self.white_to_move:
    #         return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
    #     else:
    #         return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    # def square_under_attack(self, row, col):
    #     '''
    #     Determine if enemy can attack the square row col
    #     '''
    #     self.white_to_move = not self.white_to_move  # switch to opponent's point of view
    #     opponents_moves = self.getAllPossibleMoves()
    #     self.white_to_move = not self.white_to_move
    #     for move in opponents_moves:
    #         if move.end_row == row and move.end_col == col:  # square is under attack
    #             return True
    #     return False

    def check_pins_and_checks(self):
        pins = []  # squares pinned and the direction it's pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False

        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if self.is_valid_position(end_row, end_col):
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_row, end_col,
                                            direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (i == 1 and enemy_type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append(
                                    (end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2),
                        (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if self.is_valid_position(end_row, end_col):
                end_piece = self.board[end_row][end_col]
                # enemy knight attacking a king
                if end_piece[0] == enemy_color and end_piece[1] == "N":
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks

    def get_all_possible_moves(self) -> list[Move.Move]:
        """
        Get all possible and valid moves for the current state of the game.

        Returns:
            list[Move]: A list of all possible and valid moves.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    # calls appropriate move function based on piece type
                    self.move_functions[piece](row, col, moves)
        return moves

    def get_pawn_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Generate valid moves for a pawn at a given position.

        Args:
        - row: int, the row of the pawn
        - col: int, the column of the pawn
        - moves: list[Move], list of valid moves

        Returns:
        - None
        """

        self.pawn_moves(row, col, moves)

    def get_rock_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Generates possible moves for a rook at the given row and column and adds them to the moves list.

        Args:
            row (int): The row of the rook.
            col (int): The column of the rook.
            moves (list[Move.Move]): The list of possible moves to be updated.

        Returns:
            None
        """
        self.rock_moves(row, col, moves)

    def get_knight_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Get the knight moves for the given row and column, and update the list of moves accordingly.

        Args:
            start: A tuple representing the start position of the move.
            end: A tuple representing the end position of the move.
            moves: A list of Move objects representing possible moves.

        Returns:
            None
        """
        self.knight_moves(row, col, moves)

    def get_bishop_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Get the bishop moves for the given row and column, and update the list of moves accordingly.

        Args:
            start: A tuple representing the start position of the move.
            end: A tuple representing the end position of the move.
            moves: A list of Move objects representing possible moves.

        Returns:
            None
        """
        self.bishop_moves(row, col, moves)

    def get_queen_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Get the queen moves for the given row and column, and update the list of moves accordingly.

        Args:
            start: A tuple representing the start position of the move.
            end: A tuple representing the end position of the move.
            moves: A list of Move objects representing possible moves.

        Returns:
            None
        """
        self.bishop_moves(row, col, moves)
        self.rock_moves(row, col, moves)

    def get_king_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Get all the possible moves for the king at the given position and 
        update the moves array with the valid moves. The parameters are the 
        row and column of the king, and the list of all available moves. 
        This function does not return anything.
        """
        # self.king_moves(row, col, moves)
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
                        f"{ally_color}K", row, col)

    def block_check_valid_squares(self, check: tuple[int, int], king_row: int, king_col: int) -> None:
        """
        Returns a list of valid squares to block a check.

        Args:
            check (Tuple[int, int]): The location of the checking piece.
            king_row (int): The row of the king.
            king_col (int): The column of the king.

        Returns:
            List[Tuple[int, int]]: A list of valid squares to block a check.
        """
        check_row: int = check[0]
        check_col: int = check[1]
        piece_checking: int = self.board[check_row][check_col]
        valid_squares: list[tuple[int, int]] = []

        # if knight, must capture the knight or move your king, other pieces can be blocked
        if piece_checking[1] == "N":
            valid_squares = [(check_row, check_col)]
        else:
            for i in range(1, 8):
                # check[2] and check[3] are the direction of the checking piece.
                valid_square = (
                    king_row + check[2] * i, king_col + check[3] * i)
                valid_squares.append(valid_square)

                # once you get to piece and check
                if valid_square[0] == check_row and valid_square[1] == check_col:
                    break

        return valid_squares

    def filter_moves_to_block_check(self, moves: list[Move.Move], valid_squares: list[tuple[int, int]]) -> list[Move.Move]:
        # get rid of any moves that don't block check or move king
        for i in range(len(moves)-1, -1, -1):
            # move doesn't move king so it must block or capture
            if moves[i].piece_moved[1] != "K":
                # move doesn't block or capture piece
                if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                    moves.remove(moves[i])
