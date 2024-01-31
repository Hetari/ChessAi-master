class CastleRights:
    def __init__(self,
                 white_king_side: bool,
                 white_queen_side: bool,
                 black_king_side: bool,
                 black_queen_side: bool,
                 ) -> None:
        self.white_king_side: bool = white_king_side
        self.white_queen_side: bool = white_queen_side
        self.black_king_side: bool = black_king_side
        self.black_queen_side: bool = black_queen_side
