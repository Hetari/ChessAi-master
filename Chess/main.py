import random
from src.const import *
import view.Board as Board
import src.db as db
import src.ChessEngine as ChessEngine
import pygame as p
import multiprocessing
import json
import threading


def play_music_thread(sound_manager, music_file, loops, volume):
    sound_manager.play_music(music_file, loops, volume)


def main():
    database = db.Database()
    with database:
        global current_game_id
        database.create_tables()
        database.create_new_game()
        current_game_id = database.get_game_id()

    board = Board.Board()

    # initialize the game and global variables
    flags, screen, clock, game_state, valid_moves, square_selected, player_clicks, smart_finder, sound_manager = board.initialize_game()

    # load the images on the board and the sounds effects once
    board.load_images()
    capture_path = "capture.mp3"
    castle_path = "castle.mp3"
    check_path = "check.mp3"
    game_start_path = "game_start.mp3"
    lose_path = "lose.mp3"
    move_path = "move.mp3"
    notify_path = "notify.mp3"
    win_path = "win.mp3"

    game_start_sound = threading.Thread(
        target=play_music_thread, args=(sound_manager, game_start_path, 1, 0.5)
    )

    game_start_sound.start()

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
        capture_sound = threading.Thread(
            target=play_music_thread, args=(
                sound_manager, capture_path, 1, 0.2)
        )
        check_sound = threading.Thread(
            target=play_music_thread, args=(sound_manager, check_path, 1, 0.5)
        )
        lose_sound = threading.Thread(
            target=play_music_thread, args=(sound_manager, lose_path, 1, 0.5)
        )
        move_sound = threading.Thread(
            target=play_music_thread, args=(sound_manager, move_path, 1, 0.5)
        )
        win_sound = threading.Thread(
            target=play_music_thread, args=(sound_manager, win_path, 1, 0.5)
        )

        flags["is_human_turn"] = (game_state.white_to_move and is_player_one_human) or (
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
        if not flags["game_over"] and not flags["is_human_turn"] and not flags["move_undo"]:
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

                if ai_move.is_pawn_promotion:
                    game_state.promotion_choice = random.choice(
                        ["Q", "R", "B", "N"])

                game_state.make_move(ai_move)
                flags["animate"] = True
                flags["move_made"] = True
                flags["ai_thinking"] = False

        # If a move was made, update the valid moves
        if flags["move_made"]:
            if flags["animate"]:
                board.animate_move(
                    game_state.moves_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            flags["move_made"] = False
            flags["animate"] = False
            flags["move_undo"] = False

            if len(game_state.moves_log) != 0 and game_state.moves_log[-1].piece_captured != "--":
                capture_sound.start()
            elif game_state.in_check:
                check_sound.start()
            else:
                move_sound.start()

        if game_state.check_mate:
            lose_sound.start() if game_state.white_to_move else win_sound.start()

            play_again, square_selected, player_clicks = board.show_modal(
                screen, p, "Black" if game_state.white_to_move else "White" +
                " wins", game_state, flags
            )

            database = db.Database()
            with database:
                if play_again:
                    # restart the game
                    game_state, valid_moves, square_selected, player_clicks, flags = board.reload_game(
                        flags)
                    database.create_new_game()

                else:
                    board.handle_quit(flags)

        if game_state.stale_mate:
            database = db.Database()
            with database:
                database.update_winner_into_game("Stalemate", current_game_id)
            board.show_modal(
                screen, p, "Stalemate...", game_state, flags
            )
        if flags["running"]:
            board.draw_game_state(screen, game_state,
                                  valid_moves, square_selected)
            clock.tick(MAX_FPS)
            p.display.flip()

    serialized_list = json.dumps(
        game_state.moves_log,
        default=lambda obj: obj.__json__()
    )
    database = db.Database()
    with database:
        database.update_winner_into_game(
            "Black" if game_state.white_to_move else "White", current_game_id
        )

        database.insert_moves_log(
            current_game_id,
            serialized_list
        )


if __name__ == "__main__":
    main()
