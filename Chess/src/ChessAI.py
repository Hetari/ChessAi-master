import random
import src.Move as Move


class ChessAI:
    def __init__(self) -> None:
        pass

    def find_random_move(self, valid_moves: list[Move.Move]) -> Move.Move:
        return random.choice(valid_moves)
