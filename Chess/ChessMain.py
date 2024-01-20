from const import *
import ChessEngine
import Move
import Board
import pygame as p
import numpy as np


def handle_key_events(event, game_state, flags):
    # changing themes
    if event.key == p.K_k:
        config.change_theme()

    elif event.key in [p.K_ESCAPE, p.K_q]:
        flags["running"] = False

    elif event.key == p.K_z:
        game_state.undo_move()
        flags["move_flag"] = True


def get_square_and_clicks(p):
    location = p.mouse.get_pos()
    return location[1] // SQ_SIZE, location[0] // SQ_SIZE


def handle_mouse_events(square_selected, player_clicks, game_state, valid_moves, flags):
    global p
    row, col = get_square_and_clicks(p)

    if square_selected == (row, col):
        square_selected, player_clicks = (), []

    else:
        square_selected = (row, col)
        player_clicks.append(square_selected)

    if len(player_clicks) == 2:
        move = Move.Move(player_clicks[0], player_clicks[1], game_state.board)

        if move in valid_moves:
            game_state.make_move(move)
            flags["move_flag"] = True

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
