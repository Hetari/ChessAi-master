from const import *
import ChessEngine
import Move
import Board
import pygame as p
import numpy as np


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
    move_flag = False

    board.load_images()  # do this only once, before the while loop
    running = True
    # keep track of last click
    square_selected = ()
    # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    player_clicks = []
    while running:
        for event in p.event.get():
            # Key handler
            if event.type == p.KEYDOWN:
                # changing themes
                if event.key == p.K_k:
                    config.change_theme()

                elif event.key in [p.K_ESCAPE, p.K_q]:
                    running = False

                elif event.key == p.K_z:
                    game_state.undo_move()
                    move_flag = True

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

                    # Here we need the __eq__ method to check if the move is valid, so we override the __eq__ method in the Move class
                    if move in valid_moves:
                        game_state.make_move(move)
                        move_flag = True

                    # After the piece moved, unselect it.
                    square_selected = ()
                    player_clicks = []

        if move_flag:
            # previous_valid_moves = valid_moves
            valid_moves = game_state.get_valid_moves()
            move_flag = False

        board.draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
