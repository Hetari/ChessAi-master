import random
import src.Move as Move
import src.ChessEngine as ChessEngine
from src.const import *
from functools import lru_cache, cache


class ChessAI:
    def __init__(self) -> None:
        self.CHECKMATE: int = 1000
        self.STALEMATE: int = 0
        self.DEPTH: int = 3
        self.piece_score: dict[str, int] = {
            "K": 0,
            "Q": 11,
            "R": 5,
            "B": 3,
            "N": 3,
            "p": 1,
        }

    def find_random_move(self, valid_moves: list[Move.Move]) -> Move.Move:
        return random.choice(valid_moves)

    def find_best_move(self, game_state: ChessEngine.GameState, valid_moves: list[Move.Move]) -> Move.Move:
        """
        Finds the best move for the current player given the game state and valid moves.

        Args:
        game_state (ChessEngine.GameState): The current game state.
        valid_moves (list[Move.Move]): The list of valid moves for the current player.

        Returns:
        Move.Move: The best move to be made.
        """
        # Initialize variables
        turn_multiplier: int = 1 if game_state.white_to_move else -1
        opponent_min_max_score: int = self.CHECKMATE
        best_passed_move: Move.Move = None
        random.shuffle(valid_moves)

        # Iterate through valid moves
        for player_move in valid_moves:
            game_state.make_move(player_move)
            if game_state.stale_mate:
                opponent_max_score = self.STALEMATE
            elif game_state.check_mate:
                opponent_max_score = -self.CHECKMATE
            else:
                opponent_moves = game_state.get_valid_moves()
                opponent_max_score = -self.CHECKMATE
                for opponent_move in opponent_moves:
                    game_state.make_move(opponent_move)
                    game_state.get_valid_moves()
                    if game_state.checkmate:
                        score = self.CHECKMATE
                    elif game_state.stalemate:
                        score = self.STALEMATE
                    else:
                        score = -turn_multiplier * \
                            self.score_material(game_state.board)
                    if score > opponent_max_score:
                        opponent_max_score = score
                    game_state.undo_move()
            if opponent_max_score < opponent_min_max_score:
                opponent_min_max_score = opponent_max_score
                best_player_move = player_move
            game_state.undo_move()
        return best_passed_move

    def score_material(self, board: list[str]) -> int:
        """
        Calculate the material score of the board.

        Args:
        self: instance of the class
        board: 2D list representing the game board

        Returns:
        int: the material score of the board
        """
        score: int = 0
        for row in board:
            for square in row:
                if square[0] == "w":  # if square belongs to white player
                    # add the piece score to the total score
                    score += self.piece_score[square[1]]
                elif square[0] == "b":  # if square belongs to black player
                    # subtract the piece score from the total score
                    score -= self.piece_score[square[1]]
        return score

    def score_board(self, game_state: ChessEngine.GameState) -> int:
        # a positive score is good for white, a negative score is good for black
        if game_state.check_mate:
            if game_state.white_to_move:
                return -self.CHECKMATE
            else:
                return self.CHECKMATE
        elif game_state.stale_mate:
            return self.STALEMATE

        score: int = 0
        for row in game_state.board:
            for square in row:
                if square[0] == "w":  # if square belongs to white player
                    # add the piece score to the total score
                    score += self.piece_score[square[1]]
                elif square[0] == "b":  # if square belongs to black player
                    # subtract the piece score from the total score
                    score -= self.piece_score[square[1]]
        return score

    def find_best_move_min_max(self, game_state: ChessEngine.GameState, valid_moves: list[Move.Move]):
        global next_move
        # next_move = None
        self.find_move_min_max(game_state, valid_moves,
                               DEPTH, game_state.white_to_move)

        return next_move

    # @cache
    def find_move_min_max(self, game_state: ChessEngine.GameState,
                          valid_moves: list[Move.Move], depth: int, is_white_move: bool):
        """
        Find the best move using the minimax algorithm with alpha-beta pruning.

        Args:
            game_state (ChessEngine.GameState): The current game state.
            valid_moves (list[Move.Move]): List of valid moves.
            depth (int): The depth to search in the game tree.
            is_white_move (bool): Boolean indicating if it's white's turn to move.

        Returns:
            int: The best score for the current player.
        """

        global next_move  # keep track of the best move found so far

        # Base case: if depth is 0, return the material score
        if depth == 0:
            return self.score_material(game_state.board)

        if game_state.white_to_move:
            max_score = -self.CHECKMATE
            for move in valid_moves:
                game_state.make_move(move)
                next_moves = game_state.get_valid_moves()

                # recursive call for the opponent's move
                score = self.find_move_min_max(
                    game_state, next_moves, depth - 1, False)
                if score > max_score:
                    max_score = score

                    # update the best move if at the specified depth
                    if depth == DEPTH:
                        next_move = move

                # undo the move for backtracking
                game_state.undo_move()
            return max_score

        else:
            min_score = self.CHECKMATE
            for move in valid_moves:
                game_state.make_move(move)
                next_moves = game_state.get_valid_moves()
                score = self.find_move_min_max(
                    game_state, next_moves, depth - 1, True)
                if score < min_score:
                    min_score = score
                    if depth == DEPTH:
                        next_move = move
                game_state.undo_move()
            return min_score
