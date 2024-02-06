from src.const import *
import view.Board as Board
import pygame as p
import multiprocessing
import src.db as db


def main():
    database = db.Database()
    with database:
        database.create_tables()
        database.create_new_game()

    board = Board.Board()

    # initialize the game and global variables
    flags, screen, clock, game_state, valid_moves, square_selected, player_clicks, smart_finder = board.initialize_game()

    # load the images on the board
    board.load_images()

    return_queue = multiprocessing.Queue()
    move_finder_process = multiprocessing.Process(
        target=smart_finder.find_best_move,
        args=(
            game_state,
            valid_moves,
            return_queue,
        )
    )

    is_player_one_human: bool = True
    is_player_tow_human: bool = True

    while flags["running"]:
        flags["is_human_turn"]: bool = (game_state.white_to_move and is_player_one_human) or (
            not game_state.white_to_move and is_player_tow_human)

        for event in p.event.get():
            if event.type == p.QUIT:
                board.handle_quit(flags)

            # Mouse handler
            square_selected, player_clicks = board.handle_mouse_events(
                event, square_selected, player_clicks, game_state, valid_moves, flags)

            # Key handler
            game_state, valid_moves, square_selected, player_clicks, flags = board.handle_key_events(
                event, game_state, flags, square_selected, player_clicks, valid_moves, move_finder_process)

        # Ai move finder logic
        if not flags["game_over"] and not flags["is_human_turn"] and not flags["move_undone"]:
            if not flags["ai_thinking"]:
                flags["ai_thinking"] = True
                print("Thinking...")

                # To pass data between processes
                return_queue = multiprocessing.Queue()
                move_finder_process = multiprocessing.Process(
                    target=smart_finder.find_best_move,
                    args=(
                        game_state,
                        valid_moves,
                        return_queue,
                    )
                )
                # Call the process, the same as smart_finder.find_best_move(game_state, valid_moves)
                move_finder_process.start()

            if not move_finder_process.is_alive():
                print("Done thinking...")
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = smart_finder.find_random_move(valid_moves)

                game_state.make_move(ai_move)
                flags["animate"] = True
                flags["move_made"] = True
                flags["ai_thinking"] = False

        # If a move was made, update the valid moves
        if flags["move_made"]:
            if flags["animate"]:
                board.animate_move(
                    game_state.moves_log[-1], screen, game_state.board, clock)
            # print("valid_moves 1: ", len(valid_moves))
            valid_moves = game_state.get_valid_moves()
            flags["move_made"] = False
            flags["animate"] = False
            flags["move_undone"] = False
            # print("valid_moves 2: ", len(valid_moves))
            database = db.Database()
            with database:
                current_game_id = database.get_game_id()
                database.insert_into_logs(
                    current_game_id, "Black" if game_state.white_to_move else "White", game_state.moves_log[-1].get_chess_notation())

        if game_state.check_mate:
            database = db.Database()
            with database:
                game_id = database.get_game_id()
                database.update_winner_into_game(
                    "Black" if game_state.white_to_move else "White", game_id)

            play_again, square_selected, player_clicks = board.show_modal(
                screen, p, "Check mate! press `z` to undo move", game_state, flags)

            if play_again:
                # restart the game
                game_state, valid_moves, square_selected, player_clicks, flags = board.reload_game(
                    flags)

            else:
                board.handle_quit(flags)

        if game_state.stale_mate:
            database = db.Database()
            with database:
                game_id = database.get_game_id()
                database.update_winner_into_game("Stalemate", game_id)

        # if game_state.in_check:
        #     print(f"in_check: {game_state.in_check}")

        board.draw_game_state(screen, game_state, valid_moves, square_selected)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
