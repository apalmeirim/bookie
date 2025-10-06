import sqlite3

DB_NAME = "books.db"

def create_table():
    execute("""
                   CREATE TABLE IF NOT EXISTS books(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   author TEXT,
                   year INTEGER,
                   genre TEXT,
                   rating INTEGER,
                   notes TEXT)
        """)



def execute(query, params = (), fetch=False):
    """Execute a query. If fetch is True, return fetched results, else return number of affected rows."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.rowcount
