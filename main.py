from db import create_table, add_book, delete_book, list_books

def main():
    create_table()

    while True:
        print("1. Add book")
        print("2. List books")
        print("3. Delete book")
        print("4. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            year = int(input("Year: "))
            genre = input("Genre: ")
            rating = int(input("Rating (1-5): "))
            notes = input("Notes: ")
            add_book(title, author, year, genre, rating, notes)

        elif choice == "2":
            books = list_books()
            for b in books:
                print(b)

        elif choice == "3":
            book_id = int(input("Enter book ID to delete: "))
            delete_book(book_id)

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()