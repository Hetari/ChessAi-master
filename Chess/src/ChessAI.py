# import random
import random
import src.Move as Move
import src.ChessEngine as ChessEngine
# from functools import lru_cache, cache


class ChessAI:
    def __init__(self) -> None:
        self.CHECKMATE: int = 1000
        self.STALEMATE: int = 0
        self.DEPTH: int = 4
        self.piece_score: dict[str, int] = {
            "K": 0,
            "Q": 9,
            "R": 5,
            "B": 3,
            "N": 3,
            "p": 1,

        }
        self.knight_scores: list[list[int]] = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.bishop_scores: list[list[int]] = [
            [4, 3, 2, 1, 1, 2, 3, 4],
            [3, 4, 3, 2, 2, 3, 4, 3],
            [2, 4, 4, 3, 3, 4, 4, 2],
            [1, 2, 4, 4, 4, 4, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [2, 3, 3, 3, 3, 3, 3, 2],
            [3, 4, 4, 4, 4, 4, 4, 3],
            [4, 3, 3, 4, 4, 3, 3, 4],
        ]

        self.queen_scores: list[list[int]] = [
            [1, 1, 1, 3, 1, 1, 1, 1],
            [1, 2, 3, 3, 3, 1, 1, 1],
            [1, 4, 3, 3, 3, 3, 2, 1],
            [1, 2, 3, 3, 4, 3, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 4, 3, 3, 3, 3, 2, 1],
            [1, 1, 2, 3, 3, 1, 1, 1],
            [1, 1, 1, 3, 1, 1, 1, 1],
        ]

        self.rock_scores: list[list[int]] = [
            [4, 3, 4, 4, 4, 4, 3, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 1, 2, 2, 2, 2, 1, 1],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 3, 4, 4, 4, 4, 3, 4],
        ]

        self.white_pawn_scores: list[list[int]] = [
            [8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8],
            [5, 6, 6, 7, 7, 6, 6, 5],
            [2, 3, 3, 5, 5, 3, 3, 2],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.black_pawn_scores: list[list[int]] = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [2, 3, 3, 5, 5, 3, 3, 2],
            [5, 6, 6, 7, 7, 6, 6, 5],
            [8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8],
        ]

        # self.knight_scores: list[list[int]] = [
        #     [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
        #     [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
        #     [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
        #     [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
        #     [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
        #     [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
        #     [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
        #     [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]
        # ]

        # self.bishop_scores: list[list[int]] = [
        #     [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
        #     [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
        #     [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
        #     [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
        #     [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
        #     [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
        #     [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
        #     [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]
        # ]

        # self.rook_scores: list[list[int]] = [
        #     [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        #     [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
        #     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        #     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        #     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        #     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        #     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
        #     [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]
        # ]

        # self.queen_scores: list[list[int]] = [
        #     [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
        #     [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
        #     [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
        #     [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
        #     [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
        #     [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
        #     [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
        #     [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]
        # ]

        # self.pawn_scores: list[list[int]] = [
        #     [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
        #     [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
        #     [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
        #     [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
        #     [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
        #     [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
        #     [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
        #     [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
        # ]

        self.piece_position_scores: dict[str, callable] = {
            "N": self.knight_scores,
            "B": self.bishop_scores,
            "R": self.rock_scores,
            "Q": self.queen_scores,
            "wp": self.white_pawn_scores,
            "bp": self.black_pawn_scores,
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

    def find_best_move(self, game_state: ChessEngine.GameState, valid_moves: list[Move.Move]) -> Move.Move:
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
        self.find_move_nega_max_alpha_beta(
            game_state, valid_moves,
            self.DEPTH, -self.CHECKMATE, self.CHECKMATE, 1 if game_state.white_to_move else -1
        )

        return next_move

    def find_best_move_greedy(self, game_state: ChessEngine.GameState, valid_moves) -> Move.Move:
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

    def find_best_move_min_max(self, game_state, valid_moves) -> Move.Move:
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
                          valid_moves: list[Move.Move], depth: int, is_white_move: bool) -> int:
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

    def find_move_nega_max_alpha_beta(self, game_state: ChessEngine.GameState, valid_moves: list[Move.Move], depth: int, alpha: int, beta: int, turn_multiplier: int) -> int:
        global next_move

        if depth == 0:
            return turn_multiplier * self.score_board(game_state)

        # TODO: Move ordering
        max_score = -self.CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = -self.find_move_nega_max_alpha_beta(
                game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
            if score > max_score:
                max_score = score
                if depth == self.DEPTH:
                    next_move = move
                    print(move.get_chess_notation(), max_score)

            game_state.undo_move()

            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break

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
        for row in range(len(game_state.board)):
            for col in range(len(game_state.board[row])):
                square = game_state.board[row][col]
                if square != "--":
                    piece_position_score = 0
                    if square[1] != "K":
                        if square[1] == "p":
                            piece_position_score = self.piece_position_scores[square][row][col]
                        else:
                            piece_position_score = self.piece_position_scores[square[1]][row][col]

                    if square[0] == "w":
                        # add the piece score to the total score
                        score += self.piece_score[square[1]
                                                  ] + piece_position_score * 0.1
                    elif square[0] == "b":
                        # subtract the piece score from the total score
                        score -= self.piece_score[square[1]
                                                  ] + piece_position_score * 0.1
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
