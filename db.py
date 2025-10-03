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

def add_book(title, author, year, genre, rating, notes):
    execute("""
                    INSERT INTO books (title, author, year, genre, rating, notes)
                    VALUES (?,?,?,?,?,?)""", (title, author, year, genre, rating, notes))
    
def delete_book(book_id):
    execute("DELETE FROM books WHERE id = ?", (book_id,))

def list_books():
    return execute("SELECT * FROM books", fetch=True)


def execute(query, params = (), fetch=False):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()
