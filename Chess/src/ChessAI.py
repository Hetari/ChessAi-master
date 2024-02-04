import random
import src.Move as Move
import src.ChessEngine as ChessEngine
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
            opponents_moves = game_state.get_valid_moves()

            # Evaluate opponent's moves
            if game_state.check_mate:
                opponents_max_score: int = self.CHECKMATE
            elif game_state.stale_mate:
                opponents_max_score = self.STALEMATE
            else:
                opponents_max_score = -self.CHECKMATE
                for opponents_move in opponents_moves:
                    game_state.make_move(opponents_move)
                    game_state.get_valid_moves()

                    # Check for checkmate or stalemate
                    if game_state.check_mate:
                        score: int = self.CHECKMATE
                    elif game_state.stale_mate:
                        score: int = self.STALEMATE
                    else:
                        score: int = -turn_multiplier * \
                            self.score_material(game_state.board)

                    # Update opponent's max score
                    if score > opponents_max_score:
                        opponents_max_score = score
                    game_state.undo_move()

            # Update best move based on opponent's max score
            if opponents_max_score < opponent_min_max_score:
                opponent_min_max_score = opponents_max_score
                best_passed_move = player_move
            game_state.undo_move()

        return best_passed_move

    # @lru_cache(maxsize=128,)
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
