import pygame as p
from Chess import ChessEngine


WIDTH = HEIGHT = 512  # 400 is another option
DIMENSION = 8  # dimension is 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation
IMAGES = {}


def load_images() -> None:
    """
    ### Load and scale images for each game piece.

    This function loads and scales images for each game piece using the Pygame library.
    The function iterates over a range of game pieces and loads the corresponding image
    from the 'images' directory. The loaded image is then scaled to the specified size
    using the 'transform.scale' function from the Pygame library. The scaled image is
    stored in the 'IMAGES' dictionary with the corresponding game piece as the key.

    Parameters:
        `None`

    Returns:
        `None`
    """
    # note: we can access an image by saying "IMAGES[1]"
    for piece in range(1, 13):
        IMAGES[piece] = p.transform.scale(p.image.load(
            f'images/{piece}.png'), (SQ_SIZE, SQ_SIZE))
