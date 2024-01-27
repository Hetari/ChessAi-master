import numpy as np
import Move
import pygame as p


class GameState():
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
        self.in_check: bool = False
        self.pins: list = []
        self.checks: list = []

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

        # Update the king location
        self.__update_king_location(move.piece_moved, move.end_row, move.end_col)

    def undo_move(self):
        """
        Undoes the last move made in the game.
        This method removes the last move from the move log and updates the board accordingly. If there are no moves in the move log, the method returns without making any changes to the game state.

        Args:
            None

        Returns:
            None
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            # update the king's position if needed
            self.__update_king_location(
                move.piece_moved, move.end_row, move.end_col)

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
        king_row, king_col = self.__get_king_location()

        if self.in_check == True:
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                # to block check you must move a piece into one of the squares between the enemy piece and the king
                check: tuple[int] = self.checks[0]
                valid_squares = []
                valid_squares = self.__block_check_valid_squares(
                    check, king_row, king_col)

                moves: list[Move.Move] = self.__filter_moves_to_block_check(
                    moves, valid_squares)
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()

        return moves

    def check_pins_and_checks(self):
        # squares where the allied pinned is and directions of the pinned piece
        pins = []
        # squares where enemy is applied check
        checks = []
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
        directions: tuple[tuple[int, int]] = ((-1, 0), (0, -1), (1, 0), (0, 1),
                                              (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin: tuple = ()

            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if self.__is_valid_position(end_row, end_col):
                    end_piece = self.board[end_row][end_col]

                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        # first allied piece could be pinned
                        if possible_pin == ():
                            possible_pin = (end_row, end_col,
                                            direction[0], direction[1])
                        else:
                            # second allied piece, so no pin or check possible in the direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 1.) orthogonally away from king and piece is a rock
                        # 2.) diagonally away from king and piece is bishop
                        # 3.) 1 square away diagonally from king and piece is pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king (this is necessary to prevent a king move to a square controlled by another king)
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (i == 1 and enemy_type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():
                                in_check = True
                                checks.append(
                                    (end_row, end_col, direction[0], direction[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            # enemy piece not applying checking
                            break
                else:
                    break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2),
                        (2, -1), (2, 1), (-1, -2), (1, -2))

        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                # enemy knight attaking a king
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
        # sourcery skip: merge-nested-ifs
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:  # white pawn moves
            if self.board[row-1][col] == "--":  # 1 square pawn advance
                if not piece_pinned or pin_direction == (-1, 0):
                    # (start square, end square, board)
                    moves.append(Move((row, col), (row-1, col), self.board))
                    # 2 square pawn advance
                    if row == 6 and self.board[row-2][col] == "--":
                        moves.append(
                            Move((row, col), (row-2, col), self.board))

            if col - 1 >= 0:  # capturing to the left - impossible if a pawn is standing in a far left column
                if self.board[row-1][col-1][0] == "b":  # enemy piece to capture
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(
                            Move((row, col), (row-1, col-1), self.board))

            if col + 1 <= 7:  # capturing to the right - analogical
                if self.board[row-1][col+1][0] == "b":  # enemy piece to capture
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(
                            Move((row, col), (row-1, col+1), self.board))

        else:  # black pawn moves
            if self.board[row+1][col] == "--":  # 1 suare pawn advance
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((row, col), (row+1, col), self.board))
                    if row == 1 and self.board[row+2][col] == "--":
                        moves.append(
                            Move((row, col), (row+2, col), self.board))

            if col - 1 >= 0:
                if self.board[row+1][col-1][0] == "w":
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(
                            Move((row, col), (row+1, col-1), self.board))

            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == "w":
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(
                            Move((row, col), (row+1, col+1), self.board))

    def get_rock_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                # can't remove queen from pin on rook moves, only remove it on bishop moves
                if self.board[row][col][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        # up, left, down, right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(
                                Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(
                                Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def get_knight_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Get the knight moves for the given row and column, and update the list of moves accordingly.

        Parameters:
            start: A tuple representing the start position of the move.
            end: A tuple representing the end position of the move.
            moves: A list of Move objects representing possible moves.

        Returns:
            None
        """
        piece_pinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        # up/left up/right right/up right/down down/left down/right left/up left/down
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2),
                        (2, -1), (2, 1), (-1, -2), (1, -2))
        ally_color = "w" if self.white_to_move else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    # so it's either enemy piece or empty equare
                    if end_piece[0] != ally_color:
                        moves.append(
                            Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Get the bishop moves for the given row and column, and update the list of moves accordingly.

        Parameters:
            start: A tuple representing the start position of the move.
            end: A tuple representing the end position of the move.
            moves: A list of Move objects representing possible moves.

        Returns:
            None
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # digaonals: up/left up/right down/right down/left
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(
                                Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(
                                Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def get_queen_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        """
        Get the queen moves for the given row and column, and update the list of moves accordingly.

        Parameters:
            start: A tuple representing the start position of the move.
            end: A tuple representing the end position of the move.
            moves: A list of Move objects representing possible moves.

        Returns:
            None
        """
        self.get_bishop_moves(row, col, moves)
        self.get_rock_moves(row, col, moves)

    def get_king_moves(self, row: int, col: int, moves: list[Move.Move]) -> None:
        row_moves = (-1, -1, -1, 0, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 0, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_pins_and_checks()
                    if not in_check:
                        moves.append(
                            Move((row, col), (end_row, end_col), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    def __update_king_location(self, king: str, row: int, col: int) -> None:
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
    def __is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if the given row and column are valid positions on the board.

        Args:
        row (int): The row index.
        col (int): The column index.

        Returns:
        bool: True if the position is valid, False otherwise.
        """
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])

    def __get_king_location(self) -> tuple[int, int]:
        """
        Returns the current location of the king based on whose turn it is.

        Returns:
            Tuple[int, int]: The row and column of the king.
        """
        return self.white_king_location if self.white_to_move else self.black_king_location

    def __block_check_valid_squares(self, check: tuple[int, int], king_row: int, king_col: int) -> list[tuple[int, int]]:
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

        if piece_checking[1] == "N":
            valid_squares: list[tuple[int, int]] = [(check_row, check_col)]
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

    def __filter_moves_to_block_check(self, moves: list[Move.Move], valid_squares: list[tuple[int, int]]) -> list[Move.Move]:
        # get rid of any moves that don't block check
        for i in range(len(moves) - 1, -1, -1):
            if moves[i].piece_moved[1] != "K":
                if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                    moves.remove(moves[i])
    



class Color:
    """
    class Color:
    Represents a color with a light and dark shade.

    Args:
        light: The light shade of the color.
        dark: The dark shade of the color.
    """

    def __init__(self, light: tuple[int], dark: tuple[int]):
        self.light: tuple[int] = light
        self.dark: tuple[int] = dark


class Theme:
    """
    Represents a theme for a chess game.

    Args:
        light_bg: The light background color.
        dark_bg: The dark background color.
        light_trace: The light color for trace lines.
        dark_trace: The dark color for trace lines.
        light_moves: The light color for move indicators.
        dark_moves: The dark color for move indicators.
    """

    def __init__(self, light_bg: int, dark_bg: int,
                 light_trace: int, dark_trace: int,
                 light_moves: int, dark_moves: int):
        self.bg: Color = Color(light_bg, dark_bg)
        self.trace: Color = Color(light_trace, dark_trace)
        self.moves: Color = Color(light_moves, dark_moves)


class Config():
    """
    Represents the configuration for a chess game.

    Attributes:
        themes: A list of available themes.
        idx: The index of the current theme.
        theme: The current theme.

    Methods:
        change_theme: Changes the current theme to the next one.
    """

    def __init__(self):
        self.themes: list[Theme] = []
        self._add_themes()
        self.idx: int = 0
        self.theme: Theme = self.themes[self.idx]

    def change_theme(self):
        """
        Changes the current theme to the next one.
        """
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        """
        Adds predefined themes to the list of available themes.
        """
        green: Theme = Theme(
            (234, 235, 200),
            (119, 154, 88),
            (244, 247, 116),
            (172, 195, 51),
            '#C86464',
            '#C84646',
        )

        brown: Theme = Theme(
            (235, 209, 166),
            (165, 117, 80),
            (245, 234, 100),
            (209, 185, 59),
            '#C86464',
            '#C84646',
        )
        blue: Theme = Theme(
            (229, 228, 200),
            (60, 95, 135),
            (123, 187, 227),
            (43, 119, 191),
            '#C86464',
            '#C84646',
        )

        gray: Theme = Theme(
            (120, 119, 118),
            (86, 85, 84),
            (99, 126, 143),
            (82, 102, 128),
            '#C86464',
            '#C84646',
        )

        self.themes = [green, brown, blue, gray]
