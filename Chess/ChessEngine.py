import numpy as np
import Move


class GameState():
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
        self.board = np.array([
            [7, 8, 9, 10, 11, 9, 8, 7],
            [12, 12, 12, 12, 12, 12, 12, 12],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [1, 2, 3, 4, 5, 3, 2, 1]
        ], dtype=np.int8)

        self.white_to_move = True
        self.move_log = []

    def make_move(self, move: Move) -> None:
        # Make the piece location empty
        self.board[move.start_row][move.start_col] = 0

        # Move the piece to the new location
        self.board[move.end_row][move.end_col] = move.piece_moved

        # Add the new move to the log
        self.move_log.append(move)

        # Toggle the order of moves
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """
        Undo the last move made in the game.

        This function removes the last move from the move log and updates the board accordingly. If there are no moves in the move log, the function returns without making any changes to the game state.

        Parameters:
            None

        Returns:
            None
        """
        if len(self.move_log) == 0:
            return
        move = self.move_log.pop()
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        """
        Get all possible and valid moves for the current state of the game.

        Returns:
            list[Move]: A list of all possible and valid moves.
        """
        moves = [Move.Move((6, 4), (4, 4), self.board)]
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.board[row][col]

                # check the turn of the piece is  black from 1 to 6, or white from 7 to 12

                # piece in range(7, 13) and
                if self.white_to_move:
                    if piece == 12:
                        self.get_pawn_moves(row, col, moves)
                    # elif piece == 11:
                    #     self.get_king_moves(row, col, moves)
                    # elif piece == 10:
                    #     self.get_queen_moves(row, col, moves)
                    # elif piece == 9:
                    #     self.get_bishop_moves(row, col, moves)
                    # elif piece == 8:
                    #     self.get_knight_moves(row, col, moves)
                    # elif piece == 7:
                    #     self.get_rook_moves(row, col, moves)
                else:
                    # if piece == 1:
                    #     self.get_rook_moves(row, col, moves)
                    # elif piece == 2:
                    #     self.get_knight_moves(row, col, moves)
                    # elif piece == 3:
                    #     self.get_bishop_moves(row, col, moves)
                    # elif piece == 4:
                    #     self.get_queen_moves(row, col, moves)
                    # elif piece == 5:
                    #     self.get_king_moves(row, col, moves)
                    if piece == 6:
                        self.get_pawn_moves(row, col, moves)
        # piece = self.board[row][col]
        #         move_functions = {
        #             1: self.get_rook_moves,
        #             2: self.get_knight_moves,
        #             3: self.get_bishop_moves,
        #             4: self.get_queen_moves,
        #             5: self.get_king_moves,
        #             6: self.get_pawn_moves,
        #             7: self.get_rook_moves,
        #             8: self.get_knight_moves,
        #             9: self.get_bishop_moves,
        #             10: self.get_queen_moves,
        #             11: self.get_king_moves,
        #             12: self.get_pawn_moves,
        #         }

        #     valid_pieces = range(7, 13) if self.white_to_move else range(1, 7)

        #     # check the turn of the piece is  black from 1 to 6, or white from 7 to 12
        #     if piece in valid_pieces:
        #         move_functions[piece](row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        pass


class Color:
    def __init__(self, light, dark):
        self.light = light
        self.dark = dark


class Theme:
    def __init__(self, light_bg, dark_bg,
                 light_trace, dark_trace,
                 light_moves, dark_moves):
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)


class Config():
    def __init__(self) -> None:
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247,
                      116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234,
                      100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187,
                     227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143),
                     (82, 102, 128), '#C86464', '#C84646')

        self.themes = [green, brown, blue, gray]
