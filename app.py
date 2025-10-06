from flask import Flask, render_template, request, redirect, url_for, flash
from service import list_books, add_book, get_book, update_book, delete_book, search_books
from models import Book

app = Flask(__name__)
app.secret_key = "dev"


@app.route("/")
def index():
    books = list_books(sort_by="id")
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        notes = request.form.get("notes")

        if not title:
            flash("Title is required!", "error")
            return redirect(url_for("add"))

        book = Book(
            id=None,
            title=title,
            author=author or None,
            year=int(year) if year else None,
            genre=genre or None,
            rating=int(rating) if rating else None,
            notes=notes or None
        )
        add_book(book)
        flash(f"Book '{title}' added!", "success")
        return redirect(url_for("index"))

    return render_template("add_book.html")


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    book = get_book(book_id)
    if not book:
        flash("Book not found!", "error")
        return redirect(url_for("index"))
    
    if request.method == "POST":
        updated = Book(
            id=book_id,
            title=request.form["title"],
            author=request.form.get("author"),
            year=int(request.form.get("year")) if request.form.get("year", "").isdigit() else None,
            genre=request.form.get("genre"),
            rating=int(request.form.get("rating")) if request.form.get("rating", "").isdigit() else None,
            notes=request.form.get("notes"),
        )
        update_book(book_id, updated)
        flash("Book updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("edit_book.html", book=book)


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete(book_id):
    delete_book(book_id)
    flash("Book deleted successfully!", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True) 
