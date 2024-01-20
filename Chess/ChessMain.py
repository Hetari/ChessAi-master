from const import *
import ChessEngine
import Move
import Board
import pygame as p


def handle_key_events(event: p.event.Event, game_state: ChessEngine.GameState, flags: dict[str, bool]) -> None:
    """
    Handle key events in the game, where q or escape is quit, z is undo, and k is change theme.
    """
    if event.key == p.K_k:
        game_state.config.change_theme()
    elif event.key in [p.K_ESCAPE, p.K_q]:
        flags["running"] = False
    elif event.key == p.K_z:
        game_state.undo_move()
        flags["move_flag"] = True


def get_square_and_clicks(position: p.mouse) -> tuple[int, int]:
    """
    Return the square and clicks based on the given position.

    :param position: The position to calculate the square and clicks from.
    :return: Tuple of square and clicks.
    """
    location = position
    return location[1] // SQ_SIZE, location[0] // SQ_SIZE


def handle_mouse_events(square_selected: tuple[int, int], player_clicks: list[tuple[int, int]], game_state: ChessEngine.GameState, valid_moves: list[Move.Move], flags: bool):
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
    # Get the row and column of the square clicked by the player
    row, col = get_square_and_clicks()

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
        move = Move.Move(player_clicks[0], player_clicks[1], game_state.board)
        if move in valid_moves:
            # If it's a valid move, make the move in the game state and set the move flag
            game_state.make_move(move)
            flags["move_flag"] = True
        # Reset the selected square and clear player clicks
        square_selected, player_clicks = (), []

    return square_selected, player_clicks


def main():
    board = Board.Board()

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    # Now this is my trick to improve performance, we need to get the previous valid_moves without run the function get_valid_moves
    # Now before we updating the valid_moves, we need to store it in previous_valid_moves, then update the valid_moves
    # previous_valid_moves = valid_moves
    # move_flag = False
    # running = True
    flags = {'running': True, 'move_flag': False}

    board.load_images()  # do this only once, before the while loop
    # keep track of last click
    square_selected = ()
    # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    player_clicks = []
    while flags["running"]:
        for event in p.event.get():
            if event.type == p.QUIT:
                flags["running"] = False

            # Key handler
            if event.type == p.KEYDOWN:
                handle_key_events(event, game_state, flags)

            # mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                square_selected, player_clicks = handle_mouse_events(
                    square_selected, player_clicks, game_state, valid_moves, flags)
                print(square_selected, player_clicks)

        if flags["move_flag"]:
            # previous_valid_moves = valid_moves
            valid_moves = game_state.get_valid_moves()
            flags["move_flag"] = False

        board.draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
