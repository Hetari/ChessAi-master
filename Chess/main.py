from src.const import *
import src.ChessEngine as ChessEngine
import src.Move as Move
import view.Board as Board
import pygame as p


def main():
    board = Board.Board()

    # initialize the game and global variables
    flags, screen, clock, game_state, valid_moves, square_selected, player_clicks = board.initialize_game()

    # load the images on the board
    board.load_images()

    while flags["running"]:
        for event in p.event.get():
            if event.type == p.QUIT:
                board.handle_quit(flags)

            # Key handler
            square_selected, player_clicks = board.handle_key_events(
                event, game_state, flags, square_selected, player_clicks)

            # Mouse handler
            square_selected, player_clicks = board.handle_mouse_events(
                event, square_selected, player_clicks, game_state, valid_moves, flags)

        # If a move was made, update the valid moves
        if flags["move_made"]:
            # print("valid_moves 1: ", len(valid_moves))
            valid_moves = game_state.get_valid_moves()
            flags["move_made"] = False
            # print("valid_moves 2: ", len(valid_moves))
            # clear the console

        if game_state.check_mate:
            play_again: bool = board.show_modal(
                screen, p, "Check mate! Play again?")

            if play_again:
                # restart the game
                del game_state, valid_moves, square_selected, player_clicks
                game_state = ChessEngine.GameState()
                valid_moves = game_state.get_valid_moves()
                square_selected = ()
                player_clicks = []
                flags["move_made"] = False

            else:
                board.handle_quit(flags)

        if game_state.stale_mate:
            print(f"stale_mate: {game_state.stale_mate}")

        if game_state.in_check:
            print(f"in_check: {game_state.in_check}")

        board.draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
