from src.const import *
import src.ChessEngine as ChessEngine
import src.Move as Move
import view.Board as Board
import pygame as p


def main():
    board = Board.Board()

    # initialize the game and global variables
    flags, screen, clock, game_state, valid_moves, square_selected, player_clicks, smart_finder = board.initialize_game()

    # load the images on the board
    board.load_images()

    is_player_one_ai: bool = False
    is_player_tow_ai: bool = False

    while flags["running"]:
        flags["is_human_turn"]: bool = (game_state.white_to_move and is_player_one_ai) or (
            not game_state.white_to_move and is_player_tow_ai)

        for event in p.event.get():
            if event.type == p.QUIT:
                board.handle_quit(flags)

            # Mouse handler
            square_selected, player_clicks = board.handle_mouse_events(
                event, square_selected, player_clicks, game_state, valid_moves, flags)

            # Key handler
            game_state, valid_moves, square_selected, player_clicks, flags = board.handle_key_events(
                event, game_state, flags, square_selected, player_clicks, valid_moves)

        # Ai move finder logic
        if not flags["game_over"] and not flags["is_human_turn"]:
            ai_move = smart_finder.find_best_move_min_max(
                game_state, valid_moves)

            if ai_move is None:
                print("no move found")
                ai_move = smart_finder.find_random_move(valid_moves)

            game_state.make_move(ai_move)
            flags["move_made"] = True
            flags["animate"] = True

        # If a move was made, update the valid moves
        if flags["move_made"]:
            if flags["animate"]:
                board.animate_move(
                    game_state.moves_log[-1], screen, game_state.board, clock)
            # print("valid_moves 1: ", len(valid_moves))
            valid_moves = game_state.get_valid_moves()
            flags["move_made"] = False
            flags["animate"] = False
            # print("valid_moves 2: ", len(valid_moves))

        if game_state.check_mate:
            play_again, square_selected, player_clicks = board.show_modal(
                screen, p, "Check mate! press `z` to undo move", game_state, flags)

            if play_again:
                # restart the game
                game_state, valid_moves, square_selected, player_clicks, flags = board.reload_game(
                    flags)

            else:
                board.handle_quit(flags)

        # if game_state.stale_mate:
        #     print(f"stale_mate: {game_state.stale_mate}")

        # if game_state.in_check:
        #     print(f"in_check: {game_state.in_check}")

        board.draw_game_state(screen, game_state, valid_moves, square_selected)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
