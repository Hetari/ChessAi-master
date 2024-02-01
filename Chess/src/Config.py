from src.Theme import Theme


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

        self.themes = [blue, green, brown, gray]
