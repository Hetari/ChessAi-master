from const import *
import numpy as np
import ChessEngine
import pygame as p


class Board():
    @staticmethod
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
        # Note: we reduce the size of the images by -20 to make them smaller
        # (goto draw_pieces function to see how we make the pieces in the center)
        for piece in range(1, 13):
            IMAGES[piece] = p.transform.scale(p.image.load(
                f'./Chess/images/{piece}.png'), (SQ_SIZE - 20, SQ_SIZE - 20))

    def draw_game_state(self, screen: p.Surface, game_state: ChessEngine.GameState) -> None:
        """
        Draw the current game state on the screen. This includes the board and the pieces.

        Args:
            screen (p.Surface): The surface object representing the screen to draw on.
            game_state (ChessEngine.GameState): The current game state.

        Returns:
            None
        """
        self.draw_board(screen)
        self.draw_board_notations(screen)
        self.draw_pieces(screen, game_state.board)

        # TODO: draw move log
        # TODO: draw piece highlighting

    @staticmethod
    def draw_board(screen: p.Surface) -> None:
        """
        Draw the squares on the board.

        Args:
            screen (p.Surface): The surface object representing the screen to draw on.

        Returns:
            None
        """
        colors = [p.Color(config.theme.bg.light),
                  p.Color(config.theme.bg.dark)]

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

    @staticmethod
    def draw_board_notations(screen: p.Surface) -> None:
        """
        Draws the board notations on the screen.

        Args:
            screen (pygame.Surface): The surface on which the notations are drawn.

        Returns:
            None
        """
        font = p.font.Font(None, 20)  # None for pygame default font, size 30

        ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        colors = [
            p.Color(config.theme.bg.dark),
            p.Color(config.theme.bg.light),
        ]

        for i in range(COLS):
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

    @staticmethod
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
                    # Here we add 10 to the x and 10 to the y (10 + 10 = 20) coordinates to center the piece on the square
                    screen.blit(IMAGES[piece], p.Rect(
                        col * SQ_SIZE + 10, row * SQ_SIZE + 10, SQ_SIZE, SQ_SIZE
                    ))
