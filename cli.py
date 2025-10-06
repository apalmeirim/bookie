from service import init, add_book, list_books, search_books, delete_book, get_book, update_book, export_to_csv, import_from_csv, get_stats
import os

# Try pretty printing via tabulate if available
try:
    from tabulate import tabulate
    def pretty_print(rows):
        if not rows:
            print("No books found.")
            return
        headers = ["ID", "Title", "Author", "Year", "Genre", "Rating", "Notes"]
        print(tabulate(rows, headers=headers, tablefmt="pretty"))
except Exception:
    def pretty_print(rows):
        if not rows:
            print("No books found.")
            return
        headers = ["ID", "Title", "Author", "Year", "Genre", "Rating", "Notes"]
        widths = [max(len(str(r[i])) for r in rows + [headers]) + 2 for i in range(len(headers))]
        fmt = "".join("{:<" + str(w) + "}" for w in widths)
        print(fmt.format(*headers))
        print("-" * sum(widths))
        for r in rows:
            print(fmt.format(*[str(x) if x is not None else "" for x in r]))


def input_int(prompt, allow_empty=False, default=None, minv=None, maxv=None):
    while True:
        val = input(prompt).strip()
        if val == "" and allow_empty:
            return default
        try:
            n = int(val)
            if (minv is not None and n < minv) or (maxv is not None and n > maxv):
                print(f"Please enter a number between {minv} and {maxv}.")
                continue
            return n
        except ValueError:
            print("Please enter a valid integer.")

def confirm(prompt="Are you sure? (y/n): "):
    return input(prompt).lower().startswith("y")

def add_book_flow():
    title = input("Title: ").strip()
    if not title:
        print("Title is required.")
        return
    author = input("Author: ").strip() or None
    year = input_int("Year (press Enter to skip): ", allow_empty=True, default=None)
    genre = input("Genre: ").strip() or None
    rating = input_int("Rating (1-5, Enter to skip): ", allow_empty=True, default=None, minv=1, maxv=5)
    notes = input("Notes: ").strip() or None
    add_book(title, author, year, genre, rating, notes)
    print("Book added.")

def list_books_flow():
    sort_by = input("Sort by (id/title/author/year/genre/rating) [leave empty for default id]: ").strip() or None
    desc = False
    if sort_by:
        desc = input("Descending order? (y/N): ").lower().startswith("y")
    rows = list_books(sort_by=sort_by, desc=desc)
    pretty_print(rows)

def search_flow():
    kw = input("Search keyword: ").strip()
    if not kw:
        print("Empty search.")
        return
    field = input("Search field (title/author/genre) or press Enter to search all: ").strip() or None
    rows = search_books(kw, field=field)
    pretty_print(rows)

def update_flow():
    book_id = input_int("Enter book ID to edit: ", allow_empty=False)
    book = get_book(book_id)
    if not book:
        print("Book not found.")
        return
    print("Current values (press Enter to keep current):")
    labels = ["title", "author", "year", "genre", "rating", "notes"]
    current = dict(zip(labels, book[1:]))  # skip id
    new_values = {}
    for lab in labels:
        cur = current.get(lab)
        prompt = f"{lab.capitalize()} [{cur}]: "
        if lab in ("year", "rating"):
            val = input(prompt).strip()
            if val == "":
                new_values[lab] = None
            else:
                try:
                    nv = int(val)
                    new_values[lab] = nv
                except ValueError:
                    print(f"Invalid number for {lab}, skipping.")
                    new_values[lab] = None
        else:
            val = input(prompt).strip()
            new_values[lab] = val if val != "" else None
    # Only pass fields that are not None (user typed something)
    fields_to_update = {k:v for k,v in new_values.items() if v is not None}
    if not fields_to_update:
        print("No changes provided.")
        return
    updated = update_book(book_id, **fields_to_update)
    if updated:
        print("Book updated.")
    else:
        print("Nothing updated.")

def delete_flow():
    book_id = input_int("Enter book ID to delete: ")
    book = get_book(book_id)
    if not book:
        print("Book not found.")
        return
    print(f"About to delete: [{book[0]}] {book[1]} by {book[2]}")
    if confirm("Confirm delete? (y/N): "):
        delete_book(book_id)
        print("Book deleted.")
    else:
        print("Canceled.")

def export_flow():
    fname = input("Export filename (default books_export.csv): ").strip() or "books_export.csv"
    count = export_to_csv(fname)
    print(f"Exported {count} rows to {fname}")

def import_flow():
    fname = input("CSV filename to import: ").strip()
    if not fname or not os.path.exists(fname):
        print("File not found.")
        return
    imported = import_from_csv(fname)
    print(f"Imported {imported} rows from {fname}")

def stats_flow():
    s = get_stats()
    print(f"Total books: {s['total']}")
    print(f"Average rating: {s['avg_rating'] or 'N/A'}")
    print("Books per genre:")
    for genre, count in s['per_genre']:
        print(f"  {genre or '(unknown)'}: {count}")

def main():
    init()
    while True:
        print("\n Book Tracker — CLI")
        print("1. Add book")
        print("2. List books")
        print("3. Search books")
        print("4. Edit book")
        print("5. Delete book")
        print("6. Export CSV")
        print("7. Import CSV")
        print("8. Stats")
        print("9. Quit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_book_flow()
        elif choice == "2":
            list_books_flow()
        elif choice == "3":
            search_flow()
        elif choice == "4":
            update_flow()
        elif choice == "5":
            delete_flow()
        elif choice == "6":
            export_flow()
        elif choice == "7":
            import_flow()
        elif choice == "8":
            stats_flow()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
