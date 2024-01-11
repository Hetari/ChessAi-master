from const import *
import ChessEngine
import pygame as p
import numpy as np


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
            f'./Chess/images/{piece}.png'), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen: p.Surface, game_state: ChessEngine.GameState) -> None:
    """
    Draw the current game state on the screen. This includes the board and the pieces.

    Args:
        screen (p.Surface): The surface object representing the screen to draw on.
        game_state (ChessEngine.GameState): The current game state.

    Returns:
        None
    """
    draw_board(screen)  # draw squares on the board
    # draw pieces on top of those squares
    draw_pieces(screen, game_state.board)

    # TODO: draw move log
    # TODO: draw piece highlighting


def draw_board(screen: p.Surface) -> None:
    """
    Draw the squares on the board.

    Args:
        screen (p.Surface): The surface object representing the screen to draw on.

    Returns:
        None
    """
    colors = [p.Color("white"), p.Color("gray")]

    for row in range(ROWS):
        for col in range(COLS):
            # Determine the color of the square based on its position where (col + row) % 2) is 0 or 1, in other words:
            # if we are on (0, 0) -> 0 + 0 = 0 -> 0 % 2 = 0 (even number so the color is white)
            # or if we are on (0, 1) so 0 + 1 = 1 and 1 % 2 = 1 (odd number so the color is gray)
            color = colors[((col + row) % 2)]

            # Draw a rectangle representing the square on the screen
            p.draw.rect(
                screen,  # The surface object representing the screen to draw on
                color,   # The color of the rectangle
                p.Rect(
                    col * SQ_SIZE,   # The x-coordinate of the top-left corner of the rectangle
                    row * SQ_SIZE,   # The y-coordinate of the top-left corner of the rectangle
                    SQ_SIZE,         # The width of the rectangle
                    SQ_SIZE          # The height of the rectangle
                )
            )


def draw_pieces(screen: p.Surface, board: np.ndarray) -> None:
    pass


def main() -> None:
    """
    ### Main function

    This function initializes Pygame and sets up the game loop. The game loop
    consists of the following steps:

    1. Initialize the game state
    2. Handle events
    3. Update the game state
    4. Draw the game state
    5. Update the display
    6. Limit the game speed

    Parameters:
        `None`

    Returns:
        `None`
    """

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    game_state = ChessEngine.GameState()

    load_images()  # do this only once, before the while loop
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
