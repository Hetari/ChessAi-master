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
