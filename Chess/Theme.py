from Color import Color


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
