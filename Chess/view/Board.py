from src.Theme import Theme
from src.const import *
import src.ChessEngine as ChessEngine
import src.Move as Move
import sys
import os
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

        Args:
            `None`

        Returns:
            `None`
        """
        # Note: we reduce the size of the images by -20 to make them smaller
        # (goto draw_pieces function to see how we make the pieces in the center)
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK',
                  'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load(
                f'{os.getcwd()}/images/{piece}.png'), (SQ_SIZE - 20, SQ_SIZE - 20))

    def draw_game_state(self, screen: p.Surface, game_state: ChessEngine.GameState, valid_moves: list[Move.Move], square_selected: tuple[int]) -> None:
        """
        Draw the current game state on the screen. This includes the board and the pieces.

        Args:
            screen (p.Surface): The surface object representing the screen to draw on.
            game_state (ChessEngine.GameState): The current game state.
            valid_moves: A list of valid moves for the selected piece.
            square_selected: The coordinates of the selected square.

        Returns:
            None
        """
        self.draw_board(screen)
        self.draw_board_notations(screen)
        self.highlight_squares(
            screen, game_state, valid_moves, square_selected)
        self.draw_pieces(screen, game_state.board)

    @staticmethod
    def draw_board(screen: p.Surface) -> None:
        """
        Draw the squares on the board.

        Args:
            screen (p.Surface): The screen surface to draw on.

        Returns:
            None
        """
        colors = [
            p.Color(config.theme.bg.light),
            p.Color(config.theme.bg.dark)
        ]

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

    # @staticmethod
    def draw_board_notations(self, screen: p.Surface) -> None:
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
            self.draw_rank_notations(screen, font, ranks, color, i)

            color = colors[(i + 1) % 2]

            # Draw file notations
            self.draw_file_notations(
                screen, font, files, color, i)

    @staticmethod
    def draw_rank_notations(screen: p.Surface, font: p.font.Font, ranks: list[str], color: p.Color, i: int) -> None:
        """
        Draw rank notations on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
            font (pygame.font.Font): The font to use for the notations.
            ranks (list[str]): The list of rank notations to draw.
            color (pygame.Color): The color of the notations.
            i (int): The index of the rank notation to draw.
        """
        notation = font.render(ranks[i], True, p.Color(color))
        screen.blit(notation, (5, i * SQ_SIZE + notation.get_width()))

    @staticmethod
    def draw_file_notations(screen: p.Surface, font: p.font.Font, files: list[str], color: p.Color, i: int) -> None:
        """
        Draw file notations on the screen.

        Args:
            screen (p.Surface): The surface to draw the notations on.
            font (p.font.Font): The font to use for rendering the notations.
            files (list[str]): The list of file names to render.
            color (p.Color): The color to use for rendering the notations.
            i (int): The index of the file name to render.

        Returns:
            None
        """
        notation = font.render(files[i], True, p.Color(color))
        screen.blit(notation, (i * SQ_SIZE + SQ_SIZE -
                    notation.get_width() - 5, HEIGHT - 15))

    @staticmethod
    def draw_pieces(screen: p.Surface, board: list[str]) -> None:
        """
        Draw the pieces on the board.

        Args:
            screen (p.Surface): The surface object representing the screen to draw on.
            board (list[str]): The current board state.

        Returns:
            None
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece != "--":
                    # Here we add 10 to the x and 10 to the y (10 + 10 = 20) coordinates to center the piece on the square
                    screen.blit(IMAGES[piece], p.Rect(
                        col * SQ_SIZE + 10, row * SQ_SIZE + 10, SQ_SIZE, SQ_SIZE
                    ))

    def highlight_squares(self, screen: p.Surface, game_state: ChessEngine.GameState, valid_moves: list[Move.Move], square_selected: tuple[int]) -> None:
        """
        Highlights the squares on the screen based on the selected square and valid moves.

        Args:
            screen: The Pygame surface to draw on.
            game_state: The current state of the chess game.
            valid_moves: A list of valid moves for the selected piece.
            square_selected: The coordinates of the selected square.

        Returns:
            None
        """
        if len(game_state.moves_log) > 0:
            last_move = game_state.moves_log[-1]
            s = p.Surface((SQ_SIZE, SQ_SIZE))

            # Transparency, 0 to 255
            s.set_alpha(80)

            s.fill(p.Color(p.Color("green")))
            screen.blit(s, (last_move.end_col * SQ_SIZE,
                        last_move.end_row * SQ_SIZE))

            s.fill(p.Color(p.Color("green")))
            screen.blit(s, (last_move.start_col * SQ_SIZE,
                        last_move.start_row * SQ_SIZE))

        if game_state.in_check:
            king_row, king_col = game_state.get_king_location()
            # color: Theme = config.theme.moves.light
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            # Transparency, 0 to 255
            s.set_alpha(100)
            s.fill(p.Color("red"))
            screen.blit(s, (king_col * SQ_SIZE,
                        king_row * SQ_SIZE))

        if not square_selected:
            return

        row, col = square_selected

        if game_state.board[row][col][0] == ("w" if game_state.white_to_move else "b"):
            self.highlight_hints_squares(screen, row, col, valid_moves)

    def highlight_hints_squares(self, screen: p.Surface, row: int, col: int, valid_moves: list[Move.Move]) -> None:
        """
        Highlights the selected square and valid move squares on the screen.

        Args:
            screen: The Pygame surface to draw on.
            row: The row index of the selected square.
            col: The column index of the selected square.
            valid_moves: A list of valid moves for the selected piece.

        Returns:
            None
        """
        color: Theme = config.theme.moves.light
        # highlight selected square
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        # Transparency, 0 to 255
        s.set_alpha(150)
        s.fill(p.Color(color))
        screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

        # highlight moves from that square
        s.fill(p.Color(color))
        # s.set_alpha(100)
        for move in valid_moves:
            if move.start_row == row and move.start_col == col:
                screen.blit(s, (move.end_col * SQ_SIZE,
                            move.end_row * SQ_SIZE))

    @staticmethod
    def initialize_game():
        flags = {"running": True, "move_made": False,
                 "animate": False, "game_over": False}
        p.init()
        screen = p.display.set_mode((WIDTH, HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        game_state = ChessEngine.GameState()
        valid_moves = game_state.get_valid_moves()

        # keep track of last click
        square_selected = ()

        # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
        player_clicks = []
        return flags, screen, clock, game_state, valid_moves, square_selected, player_clicks

    def handle_key_events(self, event: p.event.Event, game_state: ChessEngine.GameState, flags: dict[str, bool], square_selected: tuple[int], player_clicks: list[tuple[int]], valid_moves: list[Move.Move]) -> None:
        """
        Handle key events in the game, where q or escape is quit, z is undo, and k is change theme.
        """
        if event.type == p.KEYDOWN:
            if event.key == p.K_k:
                config.change_theme()

            elif event.key in [p.K_ESCAPE, p.K_q]:
                self.handle_quit(flags)

            elif event.key == p.K_z:
                game_state.undo_move()
                square_selected, player_clicks = (), []
                flags["move_made"] = True
                flags["animate"] = False
                flags["game_over"] = False
            elif event.key == p.K_r:
                print("r")
                game_state, valid_moves, square_selected, player_clicks, flags = self.reload_game(
                    flags)

        return game_state, valid_moves, square_selected, player_clicks, flags

    @staticmethod
    def get_square_and_clicks(position: p.mouse) -> tuple[int, int]:
        """
        Return the square and clicks based on the given position.

        :param position: The position to calculate the square and clicks from.
        :return: Tuple of square and clicks.
        """
        location = position
        return location[1] // SQ_SIZE, location[0] // SQ_SIZE

    def handle_mouse_events(self, event: p.event, square_selected: tuple[int, int], player_clicks: list[tuple[int, int]], game_state: ChessEngine.GameState, valid_moves: list[Move.Move], flags: bool):
        """
        Handle mouse events and update game state based on player clicks.

        Args:
            square_selected (tuple): The currently selected square.
            player_clicks (list): List of player's clicks.
            game_state (GameState): The current state of the game.
            valid_moves (list): List of valid moves.
            flags (dict): Dictionary of flags.

        Returns:
            tuple: Updated square_selected.
            list: Updated player_clicks.
        """
        if not flags["game_over"] and flags["is_human_turn"]:
            if event.type == p.MOUSEBUTTONDOWN:
                row, col = self.get_square_and_clicks(p.mouse.get_pos())

                # If the same square is clicked twice, reset the selected square and clear player clicks
                if square_selected == (row, col):
                    square_selected, player_clicks = (), []
                else:
                    # If a different square is clicked, update the selected square and append it to player clicks
                    square_selected = (row, col)
                    player_clicks.append(square_selected)

                # If the player has made two clicks
                if len(player_clicks) == 2:
                    # Create a Move object using the player clicks and check if it's a valid move
                    move = Move.Move(player_clicks[0],
                                     player_clicks[1], game_state.board)
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            # If it's a valid move, make the move in the game state and set the move flag
                            print(move.get_chess_notation())
                            game_state.make_move(valid_moves[i])
                            flags["move_made"] = True
                            flags["animate"] = True
                            square_selected, player_clicks = (), []

                    if not flags["move_made"]:
                        player_clicks = [square_selected]
        # if there is not a mouse click event we will return square_selected and player_clicks that passed in the function
        return square_selected, player_clicks

    def handle_quit(self, flags):
        flags["running"] = False
        flags["game_over"] = False
        p.quit()
        sys.exit()

    def reload_game(self, flags):
        game_state = ChessEngine.GameState()
        valid_moves = game_state.get_valid_moves()
        square_selected = ()
        player_clicks = []
        for flag in flags:
            if flag != "running":
                flags[flag] = False
        return game_state, valid_moves, square_selected, player_clicks, flags

    def show_modal(self, screen: p.Surface, p: p, message: str, game_state: ChessEngine.GameState, flags: dict[str, bool]):
        # Colors
        black = (0, 0, 0)
        white = (255, 255, 255)
        result = False
        # Font
        font = p.font.Font(None, 36)

        modal_width, modal_height = 450, 200
        modal_x, modal_y = (
            WIDTH - modal_width) // 2, (HEIGHT - modal_height) // 2
        modal_surface = p.Surface((modal_width, modal_height))
        modal_surface.fill(white)
        p.draw.rect(modal_surface, black,
                    (0, 0, modal_width, modal_height), 2)

        text = font.render(message, True, black)
        text_rect = text.get_rect(
            center=(modal_width // 2, modal_height // 4))
        modal_surface.blit(text, text_rect)

        # Create "Yes" button
        yes_button_rect = p.Rect(50, modal_height // 2, 100, 50)
        p.draw.rect(modal_surface, black, yes_button_rect, 2)
        yes_text = font.render("Yes", True, black)
        yes_text_rect = yes_text.get_rect(center=yes_button_rect.center)
        modal_surface.blit(yes_text, yes_text_rect)

        # Create "No" button
        no_button_rect = p.Rect(
            modal_width - 150, modal_height // 2, 100, 50)
        p.draw.rect(modal_surface, black, no_button_rect, 2)
        no_text = font.render("No", True, black)
        no_text_rect = no_text.get_rect(center=no_button_rect.center)
        modal_surface.blit(no_text, no_text_rect)

        screen.blit(modal_surface, (modal_x, modal_y))

        p.display.flip()
        square_selected, player_clicks = (), []

        # Wait for a button click to close the modal
        waiting_for_click = True
        while waiting_for_click:
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()

                elif event.type == p.KEYDOWN:
                    if event.key == p.K_z:
                        game_state.undo_move()
                        flags["move_made"] = True
                        flags["animate"] = False
                        result = True
                        return result, square_selected, player_clicks

                elif event.type == p.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Adjust coordinates based on the modal position
                    adjusted_mouse_x = mouse_x - modal_x
                    adjusted_mouse_y = mouse_y - modal_y

                    if yes_button_rect.collidepoint(adjusted_mouse_x, adjusted_mouse_y):
                        waiting_for_click = False
                        result = True
                        return result, square_selected, player_clicks

                    elif no_button_rect.collidepoint(adjusted_mouse_x, adjusted_mouse_y):
                        waiting_for_click = False
                        result = False
                        return result, square_selected, player_clicks

        return result, square_selected, player_clicks

    def animate_move(self, move: Move.Move, screen: p.Surface, board: list[str], clock: p.time.Clock) -> None:
        """
        Animate the movement of a piece on the board.

        Args:
        - move: The move to animate.
        - board: The current state of the board.
        - clock: The game clock.

        Returns:
        None
        """
        # Define colors for alternating squares
        colors: list[p.Color] = [
            p.Color(config.theme.bg.light),
            p.Color(config.theme.bg.dark)
        ]
        # Calculate the row and column difference
        direction_row: int = move.end_row - move.start_row
        direction_col: int = move.end_col - move.start_col

        # Calculate the frame count for smooth animation
        frames_per_square: int = 10
        frame_count: int = (abs(direction_row) +
                            abs(direction_col)) * frames_per_square

        # Calculate coordinates for each frame of animation
        for frame in range(frame_count + 1):
            row, col = (move.start_row + direction_row * frame / frame_count,
                        move.start_col + direction_col * frame / frame_count)

            self.draw_board(screen)
            self.draw_pieces(screen, board)

            # erase the piece moved from it's ending square
            color: p.Color = colors[((move.end_row + move.end_col) % 2)]

            # Draw the square
            end_square: p.Rect = p.Rect(
                move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE
            )
            p.draw.rect(screen, color, end_square)

            # draw captured piece onto rectangle
            if move.piece_captured != "--":
                # Draw the piece
                end_square = p.Rect(
                    move.end_col * SQ_SIZE + 10, move.end_row * SQ_SIZE + 10, SQ_SIZE, SQ_SIZE
                )

                if move.is_en_passant_move:
                    en_passant_row = move.end_row + \
                        direction_row if move.piece_captured[1] == "w" else move.end_row - direction_row
                    end_square = p.Rect(
                        move.end_col * SQ_SIZE + 10, en_passant_row * SQ_SIZE + 10, SQ_SIZE, SQ_SIZE
                    )

                screen.blit(IMAGES[move.piece_captured], end_square)

            # TODO: is_castle_move animation

            self.draw_board_notations(screen)
            # draw moving piece
            screen.blit(IMAGES[move.piece_moved], p.Rect(
                col * SQ_SIZE + 10, row * SQ_SIZE + 10, SQ_SIZE, SQ_SIZE
            ))
            p.display.flip()
            clock.tick(60)
