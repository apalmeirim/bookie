from db import execute, create_table
import csv

ALLOWED = {"id", "title", "author", "year", "genre", "rating"}

def init():
    create_table()


def add_book(title, author=None, year=None, genre=None, rating=None, notes=None):
    execute("""
                    INSERT INTO books (title, author, year, genre, rating, notes)
                    VALUES (?,?,?,?,?,?)""", (title, author, year, genre, rating, notes))   


def list_books(sort_by=None, desc=False, limit=None):
    query = "SELECT * FROM books"
    if sort_by in ALLOWED:
        query += f" ORDER BY {sort_by} { 'DESC' if desc else 'ASC' }"
    if isinstance(limit, int) and limit > 0:
        query += f" LIMIT {limit}"
    return execute(query, fetch=True)


def get_book(book_id):
    rows = execute("SELECT * FROM books WHERE id = ?", (book_id,), fetch=True)
    return rows[0] if rows else None


def delete_book(book_id):
    execute("DELETE FROM books WHERE id = ?", (book_id,))


def update_book(book_id, **fields):
    """fields: title, author, year, genre, rating, notes (only provided ones are updated)"""
    allowed = ["title", "author", "year", "genre", "rating", "notes"]
    sets = []
    params = []
    for f in allowed:
        if f in fields and fields[f] is not None:
            sets.append(f"{f} = ?")
            params.append(fields[f])
    if not sets:
        return 0
    params.append(book_id)
    query = f"UPDATE books SET {', '.join(sets)} WHERE id = ?"
    return execute(query, tuple(params))


def search_books(keyword, field=None):
    """Search in title, author, genre by default, or a specific field if provided."""
    q = f"%{keyword}%"
    if field in {"title", "author", "genre"}:
        return execute(f"SELECT * FROM books WHERE {field} LIKE ?", (q,), fetch=True)
    return execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?", (q, q, q), fetch=True)


def export_to_csv(file_path):
    rows = list_books()
    with open(file_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "author", "year", "genre", "rating", "notes"])
        for r in rows:
            writer.writerow(r)
    return len(rows)

def import_from_csv(file_path, skip_header=True):
    imported = 0
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader, None)
        for row in reader:
            if not row:
                continue
            title = row[1] if len(row) > 1 else None
            if not title:
                continue
            author = row[2] if len(row) > 2 else None
            year = int(row[3]) if len(row) > 3 and row[3].isdigit() else None
            genre = row[4] if len(row) > 4 else None
            rating = int(row[5]) if len(row) > 5 and row[5].isdigit() else None
            notes = row[6] if len(row) > 6 else None
            add_book(title, author, year, genre, rating, notes)
            imported += 1
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