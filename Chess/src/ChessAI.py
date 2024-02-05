# import random
import random
import src.Move as Move
import src.ChessEngine as ChessEngine
# from functools import lru_cache, cache


class ChessAI:
    def __init__(self) -> None:
        self.CHECKMATE: int = 1000
        self.STALEMATE: int = 0
        self.DEPTH: int = 3
        self.piece_score: dict[str, int] = {
            "K": 0,
            "Q": 9,
            "R": 5,
            "B": 3,
            "N": 3,
            "p": 1,
        }

    def find_random_move(self, valid_moves: list[Move.Move]) -> Move.Move:
        """
        Finds and returns a random move from the list of valid moves.

        Args:
            valid_moves: A list of valid moves.

        Returns:
            A random move from the list of valid moves.
        """
        return random.choice(valid_moves)

    def find_best_move(self, game_state: ChessEngine.GameState, valid_moves: list[Move.Move]):
        """
        Finds the best move to play given the current game state and a list of valid moves.

        Args:
            game_state: The current game state.
            valid_moves: A list of valid moves.

        Returns:
            None.
        """
        # Set next_move as a global variable
        global next_move

        # Shuffle the list of valid moves because to make sure the computer doesn't always pick the same move
        random.shuffle(valid_moves)

        # Find the best move using the negamax algorithm
        self.find_move_nega_max(game_state, valid_moves,
                                self.DEPTH, 1 if game_state.white_to_move else -1)

        return next_move

    def find_best_move_greedy(self, game_state: ChessEngine.GameState, valid_moves):
        """
        Finds the best move to play using a greedy strategy given the current game state and a list of valid moves.

        Args:
            game_state: The current game state.
            valid_moves: A list of valid moves.

        Returns:
            The best move to play.
        """
        # Set the turn multiplier based on the player's turn
        turn_multiplier = 1 if game_state.white_to_move else -1

        # Initialize opponent's min-max score to checkmate value
        opponent_min_max_score = self.CHECKMATE
        best_player_move = None  # Initialize the best player move to None

        # Shuffle the valid moves to introduce randomness
        random.shuffle(valid_moves)

        # Iterate through each player move to find the best move
        for player_move in valid_moves:
            # Make the player's move on the game state
            game_state.make_move(player_move)
            # Evaluate the opponent's best response
            if game_state.stale_mate:
                opponent_max_score = self.STALEMATE
            elif game_state.check_mate:
                opponent_max_score = -self.CHECKMATE
            else:
                opponent_moves = game_state.get_valid_moves()
                opponent_max_score = -self.CHECKMATE
                # Iterate through opponent's moves to find the best response
                for opponent_move in opponent_moves:
                    game_state.make_move(opponent_move)
                    game_state.get_valid_moves()
                    if game_state.self.checkmate:
                        score = self.CHECKMATE
                    elif game_state.stale_mate:
                        score = self.STALEMATE
                    else:
                        score = -turn_multiplier * \
                            self.score_material(game_state.board)
                    if score > opponent_max_score:
                        opponent_max_score = score
                    game_state.undo_move()
            # Update the best player move if opponent's max score is lower than current min-max score
            if opponent_max_score < opponent_min_max_score:
                opponent_min_max_score = opponent_max_score
                best_player_move = player_move
            # Undo the player's move for next iteration
            game_state.undo_move()
        # Return the best move to play
        return best_player_move

    def find_best_move_min_max(self, game_state, valid_moves):
        """
        Finds the best move to play using the Min-Max algorithm given the current game state and a list of valid moves.

        Args:
            game_state: The current game state.
            valid_moves: A list of valid moves.

        Returns:
            The best move to play.
        """
        # Global variable to store the best move
        global next_move

        random.shuffle(valid_moves)
        # Find the best move using Min-Max algorithm
        self.find_move_min_max(game_state, valid_moves,
                               self.DEPTH, game_state.white_to_move)
        return next_move

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

        if is_white_move:
            # Initialize the maximum score as negative infinity
            max_score = -self.CHECKMATE
            for move in valid_moves:
                game_state.make_move(move)
                next_moves = game_state.get_valid_moves()

                # Recursive call for the opponent's move
                score = self.find_move_min_max(
                    game_state, next_moves, depth - 1, False)
                if score > max_score:
                    max_score = score

                    # Update the best move if at the specified depth
                    if depth == self.DEPTH:
                        next_move = move

                # undo the move for backtracking
                game_state.undo_move()
            return max_score

        else:
            # Initialize the minimum score as positive infinity
            min_score = self.CHECKMATE
            for move in valid_moves:
                game_state.make_move(move)
                next_moves = game_state.get_valid_moves()
                score = self.find_move_min_max(
                    game_state, next_moves, depth - 1, True)
                if score < min_score:
                    min_score = score
                    if depth == self.DEPTH:
                        next_move = move
                game_state.undo_move()
            return min_score

    def find_move_nega_max(self, game_state: ChessEngine.GameState, valid_moves: list[Move.Move], depth: int, turn_multiplier: int) -> int:
        """
        Finds the best move using the NegaMax algorithm given the current game state, a list of valid moves, depth, and turn multiplier.

        Args:
            game_state: The current game state.
            valid_moves: A list of valid moves.
            depth: The depth of the search.
            turn_multiplier: The turn multiplier.

        Returns:
            The maximum score.
        """
        global next_move

        # Base case: if depth is 0, return the score of the current board state
        if depth == 0:
            return turn_multiplier * self.score_board(game_state)

        # Initialize max_score to negative infinity
        max_score = -self.CHECKMATE

        # Iterate through each valid move
        for move in valid_moves:
            # Make the move on the game state
            game_state.make_move(move)

            # Get the valid moves for the next state
            next_moves = game_state.get_valid_moves()

            # Recursively find the score for the next state
            score = -self.find_move_nega_max(
                game_state, next_moves, depth - 1, -turn_multiplier)

            # Update max_score if the new score is higher
            if score > max_score:
                max_score = score
                if depth == self.DEPTH:
                    next_move = move

            # Undo the move for backtracking
            game_state.undo_move()

        # Return the maximum score found
        return max_score

    def score_board(self, game_state: ChessEngine.GameState) -> int:
        """
        Calculate the score of the chess board based on the pieces and game state.

        Args:
            game_state (ChessEngine.GameState): The current state of the chess game.

        Returns:
            int: The score of the chess board.
        """
        # a positive score is good for white, a negative score is good for black
        if game_state.check_mate:
            if game_state.white_to_move:
                # return checkmate score for black
                return -self.CHECKMATE
            else:
                # return checkmate score for white
                return self.CHECKMATE
        elif game_state.stale_mate:
            return self.STALEMATE

        score: int = 0
        for row in game_state.board:
            for square in row:
                if square[0] == "w":
                    # add the piece score to the total score
                    score += self.piece_score[square[1]]
                elif square[0] == "b":
                    # subtract the piece score from the total score
                    score -= self.piece_score[square[1]]
        return score

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
                if square[0] == "w":
                    score += self.piece_score[square[1]]
                elif square[0] == "b":
                    score -= self.piece_score[square[1]]
        return score
