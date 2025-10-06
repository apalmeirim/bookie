from db import execute, create_table
from models import Book
from typing import Optional, List
import csv

ALLOWED = {"id", "title", "author", "year", "genre", "rating"}

def init():
    create_table()


def add_book(book: Book) -> int:
    execute("""
                    INSERT INTO books (title, author, year, genre, rating, notes)
                    VALUES (?,?,?,?,?,?)""", (book.title, book.author, book.year, book.genre, book.rating, book.notes))   
    result = execute("SELECT last_insert_rowid()", fetch=True)
    return result [0][0] if result else None


def list_books(sort_by: str = None, desc: bool = False) -> List[Book]:
    query = "SELECT * FROM books"
    if sort_by:
        query += f" ORDER BY {sort_by} { 'DESC' if desc else 'ASC' }"
    rows = execute(query, fetch=True)
    return [Book(*row) for row in rows] 


def get_book(book_id: int) ->  Optional[Book]:
    rows = execute("SELECT * FROM books WHERE id = ?", (book_id,), fetch=True)
    return Book(*rows[0]) if rows else None


def delete_book(book_id: int) -> bool:
    execute("DELETE FROM books WHERE id = ?", (book_id,))
    return True



def update_book(book_id: int, updated_book: Book) -> bool:
    """
    Update an existing book using fields from a Book dataclass.
    Only updates fields that are not None.
    """
    fields = {
        "title": updated_book.title,
        "author": updated_book.author,
        "year": updated_book.year,
        "genre": updated_book.genre,
        "rating": updated_book.rating,
        "notes": updated_book.notes
    }

    # Keep only non-None fields (so you can partially update)
    updates = {k: v for k, v in fields.items() if v is not None}

    if not updates:
        return False  # nothing to update

    set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
    params = list(updates.values()) + [book_id]

    query = f"UPDATE books SET {set_clause} WHERE id = ?"
    execute(query, tuple(params))
    return True


def search_books(keyword: str, field: Optional[str] = None) -> List[Book]:
    """Search in title, author, or genre by default, or a specific field if provided."""
    q = f"%{keyword}%"
    if field in {"title", "author", "genre"}:
        rows = execute(f"SELECT * FROM books WHERE {field} LIKE ?", (q,), fetch=True)
    else:
        rows = execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?", (q, q, q), fetch=True
        )
    return [Book(*r) for r in rows]


def export_to_csv(file_path: str) -> int:
    books = list_books()
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "author", "year", "genre", "rating", "notes"])
        for b in books:
            writer.writerow([
                b.id, b.title, b.author, b.year, b.genre, b.rating, b.notes
            ])
    return len(books)


def import_from_csv(file_path: str, skip_header: bool = True) -> int:
    imported = 0
    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader, None)
        for row in reader:
            if not row or len(row) < 2:
                continue

            try:
                book = Book(
                    id=None,
                    title=row[1],
                    author=row[2] if len(row) > 2 else None,
                    year=int(row[3]) if len(row) > 3 and row[3].isdigit() else None,
                    genre=row[4] if len(row) > 4 else None,
                    rating=int(row[5]) if len(row) > 5 and row[5].isdigit() else None,
                    notes=row[6] if len(row) > 6 else None
                )
                add_book(book)
                imported += 1
            except Exception as e:
                print(f"Skipping row due to error: {e}")
    return imported



def get_stats():
    total = execute("SELECT COUNT(*) FROM books", fetch=True)[0][0]
    avg_rating_row = execute("SELECT AVG(rating) FROM books WHERE rating IS NOT NULL", fetch=True)
    avg_rating = round(avg_rating_row[0][0], 2) if avg_rating_row and avg_rating_row[0][0] is not None else None
    per_genre = execute("SELECT genre, COUNT(*) FROM books GROUP BY genre ORDER BY COUNT(*) DESC", fetch=True)
    return {
        "total": total,
        "avg_rating": avg_rating,
        "per_genre": per_genre
    }

