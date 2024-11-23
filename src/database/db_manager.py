import sqlite3
from config import DB_PATH

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def create_tables(self):
        """Creates necessary database tables."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_price REAL,
                    exit_price REAL,
                    volume INTEGER,
                    profit_loss REAL,
                    is_win BOOLEAN,
                    strategy TEXT
                )
            """)

    def insert_trade(self, trade):
        """Inserts a trade into the database."""
        with self.conn:
            self.conn.execute("""
                INSERT INTO trades (entry_price, exit_price, volume, profit_loss, is_win, strategy)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                trade["entry_price"],
                trade["exit_price"],
                trade["volume"],
                trade["profit_loss"],
                trade["profit_loss"] > 0,  # is_win
                trade["strategy"]
            ))

    def fetch_all_trades(self):
        """Fetches all trades from the database."""
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM trades")
            return cursor.fetchall()
