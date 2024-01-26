import numpy as np
import Move
import pygame as p


class GameState():
    """
    The GameState class keeps track of the chess board, the current player's turn, and the move history. It provides methods to make moves, undo moves, and get all possible moves for the current state of the game.

    Attributes:
        board: A 2D list representing the chess board.
        move_functions: A dictionary mapping piece types to their corresponding move functions.
        white_to_move: A boolean indicating whether it is currently white's turn to move.
        move_log: A list of Move objects representing the move history.

    Methods:
        make_move: Makes a move on the chess board.
        undo_move: Undoes the last move made in the game.
        get_valid_moves: Returns a list of all valid moves for the current state of the game.
        get_all_possible_moves: Returns a list of all possible moves for the current state of the game.
        get_pawn_moves: Generates valid moves for a pawn at a given position.
    """

    def __init__(self) -> None:
        # board is 8x8 2d list, each element of list has 2 characters
        # 0 represents an empty space
        # 1 represents a black rook
        # 2 represents a black knight
        # 3 represents a black bishop
        # 4 represents a black queen
        # 5 represents a black king
        # 6 represents a black pawn
        # 7 represents a white rook
        # 8 represents a white knight
        # 9 represents a white bishop
        # 10 represents a white queen
        # 11 represents a white king
        # 12 represents a white pawn
        self.board: np.ndarray = np.array([
            [1, 2, 3, 4, 5, 3, 2, 1],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [12, 12, 12, 12, 12, 12, 12, 12],
            [7, 8, 9, 10, 11, 9, 8, 7],
        ], dtype=np.int8)

        # Get the possible moves for each piece
        self.move_functions: dict[int, callable] = {
            1: self.get_rock_moves,
            2: self.get_knight_moves,
            3: self.get_bishop_moves,
            4: self.get_queen_moves,
            5: self.get_king_moves,
            6: self.get_pawn_moves,
            7: self.get_rock_moves,
            8: self.get_knight_moves,
            9: self.get_bishop_moves,
            10: self.get_queen_moves,
            11: self.get_king_moves,
            12: self.get_pawn_moves,
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
        # Make the piece location empty
        self.board[move.start_row][move.start_col] = 0

        # Move the piece to the new location
        self.board[move.end_row][move.end_col] = move.piece_moved

        # Add the new move to the log
        self.move_log.append(move)

        # Update the king location
        if move.piece_moved == 11:
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 5:
            self.black_king_location = (move.end_row, move.end_col)

        # Toggle the order of moves
        self.white_to_move = not self.white_to_move

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
        move: Move.Move = self.move_log.pop()
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured

        if move.piece_moved == 11:
            self.white_king_location = (move.start_row, move.start_col)
        elif move.piece_moved == 12:
            self.black_king_location = (move.start_row, move.start_col)

        self.white_to_move = not self.white_to_move

    def get_valid_moves(self) -> list[Move.Move]:
        """
        Returns a list of all valid moves for the current state of the game.

        This method calls the get_all_possible_moves method to get all possible moves and filters out the invalid moves.

        Args:
            None

        Returns:
            list[Move]: A list of all valid moves.
        """
        # generate all moves
        moves: list[Move.Move] = []

        self.in_check, self.pins, self.checks = self.check_pins_and_checks()

        if self.white_to_move:
            king_row: int = self.white_king_location[0]
            king_col: int = self.white_king_location[1]
        else:
            king_row: int = self.black_king_location[0]
            king_col: int = self.black_king_location[1]

        # * print("moves[i].piece_moved", moves[0].piece_moved)

        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                # to block check you must move a piece into one of the squares between the enemy piece and the king
                check: tuple[int] = self.checks[0]
                check_row: int = check[0]
                check_col: int = check[1]
                piece_checking: int = self.board[check_row][check_col]

                valid_squares = []
                if piece_checking in [2, 8]:
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        # check[2] and check[3] are the direction.
                        valid_square = (
                            king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)

                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break

                # get rid of any moves that don't block check
                for i in range(len(moves) - 1, -1, -1):
                    # if moves[i].piece_moved != piece_checking:
                    if moves[i].piece_moved in [5, 10]:
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
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
            enemy_is = list(range(1, 7))
            ally_is = list(range(7, 13))
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_is = list(range(7, 13))
            ally_is = list(range(1, 7))
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        # check outwards from king for pins and checks, keep track of pins
        directions: list[tuple[int, int]] = [
            (-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin: tuple = ()

            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if self.__is_valid_position(end_row, end_col):

                    end_piece = self.board[end_row][end_col]

                    # !!! and end_piece not in [5, 10]
                    if end_piece in ally_is:
                        # first allied piece could be pinned
                        if possible_pin == ():
                            possible_pin = (end_row, end_col,
                                            direction[0], direction[1])
                        else:
                            # second allied piece, so no pin or check possible in the direction
                            break
                    elif end_piece in enemy_is:
                        enemy_type = end_piece
                        # 1.) orthogonally away from king and piece is a rock
                        # 2.) diagonally away from king and piece is bishop
                        # 3.) 1 square away diagonally from king and piece is pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king (this is necessary to prevent a king move to a square controlled by another king)
                        #! if (0 <= j <= 3 and enemy_piece == 1) or \
                        #!         (4 <= j <= 7 and enemy_piece == 3) or \
                        #!     (i == 1 and enemy_piece == 6 and ((enemy_is in range(1, 7) and 6 <= j <= 7) or (enemy_is in range(7, 13) and 4 <= j <= 5))) or \
                        #! (enemy_piece == 4) or (i == 1 and enemy_piece == 5):
                        # Print statements for debugging
                        # * print(
                        # *     f"Checking direction {direction} at distance {i} from ({start_row}, {start_col})")
                        # * print(f"End piece: {end_piece}")

                        if (0 <= j <= 3 and enemy_type in [1, 7]) or \
                            (4 <= j <= 7 and enemy_type in [3, 9]) or \
                            (i == 1 and enemy_type in [6, 12] and ((enemy_type in range(1, 7) and 6 <= j <= 7) or (enemy_type in range(7, 13) and 4 <= j <= 5))) or \
                            enemy_type == 4 or \
                                (i == 1 and enemy_type in [5, 11]):
                            # * print(
                            # *     f"Checking direction {direction} at distance {i} from ({start_row}, {start_col})")
                            if possible_pin == ():
                                # * print("Check!")
                                in_check = True
                                checks.append(
                                    (end_row, end_col, direction[0], direction[1]))
                                break
                            else:
                                # * print("Pinned!")
                                pins.append(possible_pin)
                                break
                        else:
                            # * print("Not pinned!")
                            break
                else:
                    # * print("Not valid position!")
                    break
        knight_moves: tuple[tuple[int, int]] = (
            (2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        for move in knight_moves:
            end_row: int = start_row + move[0]
            end_col: int = start_col + move[1]

            if self.__is_valid_position(end_row, end_col):
                end_piece: int = self.board[end_row][end_col]
                if end_piece in enemy_is and end_piece in [2, 8]:
                    in_check = True
                    checks.append(
                        (end_row, end_col, move[0], move[1]))

        return in_check, pins, checks

    def get_all_possible_moves(self) -> list[Move.Move]:
        """
        Get all possible and valid moves for the current state of the game.

        Returns:
            list[Move]: A list of all possible and valid moves.
        """
        moves: list[Move.Move] = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.board[row][col]

                # check the turn of the piece is  black from 1 to 6, or white from 7 to 12
                if piece in range(1, 13):
                    self.move_functions.get(
                        piece, lambda *_: None)(row, col, moves)
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
        piece_pinned: bool = False
        pin_direction: tuple[int] = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.__is_valid_position(row, col) and self.white_to_move:
            # Check for empty square in front of the pawn
            if self.__is_valid_position(row + 1, col) and self.board[row - 1][col] == 0:
                if not piece_pinned or pin_direction == (-1, 0):
                    self.__append_pawn_move((row, col), (row - 1, col), moves)
                    # Check for double-step move from starting row if is in its place
                    if row == 6 and self.board[row - 2][col] == 0:
                        self.__append_pawn_move(
                            (row, col), (row - 2, col), moves)

            # Check for capturing moves, left and right
            if not piece_pinned or pin_direction == (-1, -1):
                self.__append_pawn_capture(
                    (row, col), (row - 1, col - 1), moves)

            if not piece_pinned or pin_direction == (-1, 1):
                self.__append_pawn_capture(
                    (row, col), (row - 1, col + 1), moves)

        elif self.__is_valid_position(row, col) and not self.white_to_move:
            if self.__is_valid_position(row + 1, col) and self.board[row + 1][col] == 0:
                if not piece_pinned or pin_direction == (1, 0):
                    self.__append_pawn_move((row, col), (row + 1, col), moves)
                    if row == 1 and self.board[row + 2][col] == 0:
                        self.__append_pawn_move(
                            (row, col), (row + 2, col), moves)

            if not piece_pinned or pin_direction == (1, -1):
                self.__append_pawn_capture(
                    (row, col), (row + 1, col - 1), moves)

            if not piece_pinned or pin_direction == (1, 1):
                self.__append_pawn_capture(
                    (row, col), (row + 1, col + 1), moves)

    def __append_pawn_move(self, start: tuple[int], end: tuple[int], moves: list[Move.Move]):
        """
        Append a pawn move to the list of moves.

        Args:
            start (tuple[int]): The starting position of the pawn move.
            end (tuple[int]): The ending position of the pawn move.
            moves (list[Move.Move]): The list of moves to append the pawn move to.

        Returns:
            None
        """
        if self.__is_valid_position(end[0], end[1]):
            moves.append(Move.Move(start, end, self.board))

    def __append_pawn_capture(self, start: tuple[int], end: tuple[int], moves: list[Move.Move]):
        """
        Appends a pawn capture move to the list of moves.

        Parameters:
            start (tuple[int]): The starting position of the pawn.
            end (tuple[int]): The ending position of the pawn after the capture.
            moves (list[Move.Move]): The list of moves to append the capture move to.

        Returns:
            None
        """
        # Check if the ending position is a valid position on the board, then:
        # Check if the captured piece is an opponent's piece, then:
        # Create a new move object and append it to the list of moves
        if self.__is_valid_position(end[0], end[1]) and ((self.white_to_move and self.board[end[0]][end[1]] in range(1, 7)) or (not self.white_to_move and self.board[end[0]][end[1]] in range(7, 13))):
            moves.append(Move.Move(start, end, self.board))

    def get_rock_moves(self,
                       row: int,
                       col: int,
                       moves: list[Move.Move],
                       directions: tuple[tuple[int]] = ((-1, 0), (0, -1), (1, 0), (0, 1),)) -> None:
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                if self.board[row][col] not in [5, 10]:
                    self.pins.remove(self.pins[i])
                break

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i

                if not self.__is_valid_position(end_row, end_col):
                    break

                if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                    end_piece: int = self.board[end_row][end_col]
                    is_enemy: bool = self.__is_enemy(end_row, end_col)

                    if end_piece == 0:
                        self.__append_rock_move(
                            (row, col), (end_row, end_col), moves
                        )
                    elif is_enemy:
                        self.__append_rock_capture(
                            (row, col), (end_row, end_col), moves
                        )
                        break
                    else:
                        break

    def __append_rock_move(self, start: tuple[int], end: tuple[int], moves: list[Move.Move]):
        """
        Append a rock move to the list of moves if the piece at the start position is a valid rock piece for the current player's turn.

        Parameters:
            start: A tuple representing the start position of the move.
            end: A tuple representing the end position of the move.
            moves: A list of Move objects representing possible moves.

        Returns:
            None
        """
        if (self.white_to_move and self.board[start[0]][start[1]] in range(7, 13)) or (not self.white_to_move and self.board[start[0]][start[1]] in range(1, 7)):
            moves.append(Move.Move(start, end, self.board))

    def __append_rock_capture(self, start: tuple[int], end: tuple[int], moves: list[Move.Move]):
        """
        Append a rock move to the list of moves if the piece at the start position is a valid rock piece for the current player's turn, and has capture.

        Parameters:
            start: A tuple representing the start position of the move.
            end: A tuple representing the end position of the move.
            moves: A list of Move objects representing possible moves.

        Returns:
            None
        """
        if (self.white_to_move and self.board[end[0]][end[1]] in range(1, 7)) or (not self.white_to_move and self.board[end[0]][end[1]] in range(7, 13)):
            moves.append(Move.Move(start, end, self.board))

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
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        self.get_rock_moves(row, col, moves, directions)

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
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        directions = (
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        )
        for direction in directions:
            end_row = row + direction[0]
            end_col = col + direction[1]

            if not self.__is_valid_position(end_row, end_col):
                continue

            if not piece_pinned:
                end_piece: int = self.board[end_row][end_col]
                is_enemy: bool = self.__is_enemy(end_row, end_col)

                if end_piece == 0 or is_enemy:
                    self.__append_rock_move(
                        (row, col), (end_row, end_col), moves
                    )

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
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)

        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]

            if not self.__is_valid_position(end_row, end_col):
                continue

            end_piece: int = self.board[end_row][end_col]
            is_enemy: bool = self.__is_enemy(end_row, end_col)

            if end_piece == 0 or is_enemy:
                if self.white_to_move:
                    self.white_king_location = (end_row, end_col)
                else:
                    self.black_king_location = (end_row, end_col)

                in_check, pins, checks = self.check_pins_and_checks()

                if not in_check:
                    self.__append_rock_move(
                        (row, col), (end_row, end_col), moves
                    )

                if self.white_to_move:
                    self.white_king_location = (row, col)
                else:
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

    def __is_enemy(self, row: int, col: int) -> bool:
        """
        Check if the given position is an enemy piece.

        Args:
        row (int): The row index.
        col (int): The column index.

        Returns:
        bool: True if the position is an enemy piece, False otherwise.
        """
        return (self.white_to_move and self.board[row][col] in range(1, 7)) or (not self.white_to_move and self.board[row][col] in range(7, 13))


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
