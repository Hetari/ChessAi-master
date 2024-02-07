import sqlite3
import os


class Database:
    __DB_LOCATION = f"{os.getcwd()}/chess.db"

    def __init__(self, db_location=None):
        if db_location is not None:
            self.db_connection = sqlite3.connect(db_location)
        else:
            self.db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.db_connection.cursor()

    def execute(self, new_data):
        self.cursor.execute(new_data)

    def create_tables(self):
        # Create game table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_played TEXT DEFAULT CURRENT_TIMESTAMP,
                winner TEXT DEFAULT NULL
            )
        """)

        # Create log table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                moves TEXT NOT NULL,
                FOREIGN KEY(game_id) REFERENCES games(id)
            )
        """)

    def create_new_game(self):
        self.cursor.execute("""
            INSERT INTO games(winner) VALUES (NULL)
        """)

    def update_winner_into_game(self, winner, game_id):
        self.cursor.execute("""
            UPDATE games SET winner = ? WHERE id = ?
        """, (winner, game_id))

    def insert_moves_log(self, game_id, moves):
        self.cursor.execute("""
            INSERT INTO logs(game_id, moves) VALUES (?, ?)
        """, (game_id, moves))

    def get_game_id(self):
        return self.cursor.execute("""
            SELECT MAX(id) FROM games
        """).fetchone()[0]

    def commit(self):
        self.db_connection.commit()

    def __del__(self):
        self.db_connection.close()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.db_connection.rollback()
            self.cursor.close()
        else:
            self.db_connection.commit()
        self.db_connection.close()
