from const import *
import ChessEngine
import Move
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
    draw_board(screen)
    draw_board_notations(screen)
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
    colors = [p.Color(config.theme.bg.light), p.Color(config.theme.bg.dark)]

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


def draw_board_notations(screen: p.Surface) -> None:
    font = p.font.Font(None, 20)  # None for pygame default font, size 30

    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    colors = [
        p.Color(config.theme.bg.dark),
        p.Color(config.theme.bg.light),
    ]

    for i in range(8):
        color = colors[i % 2]

        # Draw rank notations
        notation = font.render(ranks[i], True, p.Color(color))
        screen.blit(notation, (5, i * SQ_SIZE +
                    notation.get_width()))

        color = colors[(i + 1) % 2]

        # Draw file notations
        notation = font.render(files[i], True, p.Color(color))
        screen.blit(notation, (i * SQ_SIZE + SQ_SIZE -
                    notation.get_width() - 5, HEIGHT - 15))


def draw_pieces(screen: p.Surface, board: np.ndarray) -> None:
    """
    Draw the pieces on the board.

    Args:
        screen (p.Surface): The surface object representing the screen to draw on.
        board (np.ndarray): The current board state.

    Returns:
        None
    """
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != 0:
                screen.blit(IMAGES[piece], p.Rect(
                    col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE
                ))


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
    # keep track of last click
    square_selected = ()
    # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    player_clicks = []
    while running:
        for event in p.event.get():
            # changing themes
            if event.type == p.KEYDOWN:
                if event.key == p.K_k:
                    config.change_theme()
                elif event.key == p.K_ESCAPE or event.key == p.K_q:
                    running = False

            if event.type == p.QUIT:
                running = False

            # mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y)
                row = location[1] // SQ_SIZE
                col = location[0] // SQ_SIZE

                # user clicked the same square twice, unselect
                if square_selected == (row, col):
                    square_selected = ()
                    player_clicks = []

                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)

                if len(player_clicks) == 2:
                    move = Move.Move(
                        player_clicks[0], player_clicks[1], game_state.board)
                    print(move.get_chess_notation())
                    game_state.make_move(move)

                    square_selected = ()
                    player_clicks = []

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
