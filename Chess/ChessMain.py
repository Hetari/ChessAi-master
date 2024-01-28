import os
from const import *
import ChessEngine
import Move
import Board
import pygame as p
import sys


def initialize_game():
    flags = {'running': True, 'move_flag': False}
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


def handle_key_events(event: p.event.Event, game_state: ChessEngine.GameState, flags: dict[str, bool], square_selected: tuple[int], player_clicks: list[tuple[int]]) -> None:
    """
    Handle key events in the game, where q or escape is quit, z is undo, and k is change theme.
    """
    if event.type == p.KEYDOWN:
        if event.key == p.K_k:
            config.change_theme()

        elif event.key in [p.K_ESCAPE, p.K_q]:
            handle_quit(flags)

        elif event.key == p.K_z:
            game_state.undo_move()
            square_selected, player_clicks = (), []
            flags["move_flag"] = True
    return square_selected, player_clicks


def get_square_and_clicks(position: p.mouse) -> tuple[int, int]:
    """
    Return the square and clicks based on the given position.

    :param position: The position to calculate the square and clicks from.
    :return: Tuple of square and clicks.
    """
    location = position
    return location[1] // SQ_SIZE, location[0] // SQ_SIZE


def handle_mouse_events(event: p.event, square_selected: tuple[int, int], player_clicks: list[tuple[int, int]], game_state: ChessEngine.GameState, valid_moves: list[Move.Move], flags: bool):
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
    if event.type == p.MOUSEBUTTONDOWN:
        row, col = get_square_and_clicks(p.mouse.get_pos())

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
            if move in valid_moves:
                # If it's a valid move, make the move in the game state and set the move flag
                print(move.get_chess_notation())
                game_state.make_move(move)
                flags["move_flag"] = True
                square_selected, player_clicks = (), []
            else:
                player_clicks = [square_selected]
    # if there is not a mouse click event we will return square_selected and player_clicks that passed in the function
    return square_selected, player_clicks


def handle_quit(flags):
    flags["running"] = False
    p.quit()
    sys.exit()


def main():
    # initialize the game and global variables
    flags, screen, clock, game_state, valid_moves, square_selected, player_clicks = initialize_game()

    # load the images on the board
    board = Board.Board()
    board.load_images()

    while flags["running"]:
        for event in p.event.get():
            if event.type == p.QUIT:
                handle_quit(flags)

            # Key handler
            square_selected, player_clicks = handle_key_events(event, game_state, flags,
                                                               square_selected, player_clicks)

            # Mouse handler
            square_selected, player_clicks = handle_mouse_events(
                event, square_selected, player_clicks, game_state, valid_moves, flags)

        # If a move was made, update the valid moves
        if flags["move_flag"]:
            print("valid_moves 1: ", len(valid_moves))
            valid_moves = game_state.get_valid_moves()
            flags["move_flag"] = False
            print("valid_moves 2: ", len(valid_moves))
            # clear the console

        board.draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
