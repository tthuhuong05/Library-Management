import os
from flask import request, redirect, url_for, current_app, render_template, session
from model.book_model import BookModel

class BookController:
    def __init__(self):
        self.model = BookModel()

    def update_book(self, book_id, title, author, publisher, year, status, image_filename=None):
        """Update the details of an existing book."""
        return self.model.update_book(book_id, title, author, publisher, year, status, image_filename)

    def get_books(self):
        """Fetch the list of all books."""
        return self.model.get_books()

    def get_book_by_id(self, book_id):
        """Fetch book by ID."""
        return self.model.get_book_by_id(book_id)

    def request_books(self):
        """Fetch the list of books and render."""
        book_items = self.model.get_books()
        return render_template("list_book.html", items=book_items)

    def create_book(self):
        """Render the form to create a new book."""
        return render_template("book_form.html")

    def store_book(self, status="Available"):
      """Store a new book."""
      title = request.form.get("title")
      author = request.form.get("author")
      publisher = request.form.get("publisher")
      year = request.form.get("year")

      if year:
        year = int(year)

    # Handle file upload
      image_file = request.files.get("image")
      image_filename = None
      if image_file and image_file.filename != "":
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        ext = image_file.filename.rsplit(".", 1)[-1].lower()
        if ext in allowed_extensions:
            image_filename = image_file.filename
            upload_path = os.path.join(current_app.root_path, "static", "uploads", image_filename)
            image_file.save(upload_path)
        else:
              return "Invalid file type", 400

    # Store the book details in the model (including status)
      self.model.store_book(title=title, author=author, publisher=publisher, year=year, status=status, image_filename=image_filename)

    # Redirect to the book list page
      return redirect(url_for("show_book_list"))


    def edit_book(self, book_id):
        """Render form to edit an existing book."""
        book_item = self.model.get_book_by_id(book_id)
        if book_item:
            if request.method == 'POST':
                title = request.form['title']
                author = request.form['author']
                publisher = request.form['publisher']
                year = int(request.form['year'])
                status = request.form.get('status', 'Available')  # Ensure status is retrieved from the form

                image_file = request.files.get('image')
                image_filename = book_item['image']  # Default to current image if no new image is uploaded

                if image_file and image_file.filename != "":
                    image_filename = image_file.filename
                    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', image_filename)
                    image_file.save(upload_path)

                # Call method to update the book with new status and other fields
                if self.model.update_book(book_id, title, author, publisher, year, status, image_filename=image_filename):
                    return redirect(url_for('show_book_list'))  # Redirect to book list after update
                else:
                    return "Error updating book", 500

            return render_template("edit_book.html", book=book_item)
        return "Book not found", 404

    def delete_book(self, book_id):
        """Delete a book from the database."""
        self.model.delete_book(book_id)
        return redirect(url_for("show_book_list"))

    def search_books(self, keyword):
        """Search books by a keyword."""
        book_items = self.model.search_books(keyword)
        return book_items

    def borrow_book(self, book_id, user_id):
        """Handle borrowing a book."""
        # Update the book status to "Borrowed"
        self.model.update_book_status(book_id, "Borrowed")
        
        # Add the book to the user's borrowed books
        self.user_model.add_borrowed_book(user_id, book_id)
        
        return redirect(url_for("library"))  # Redirect back to library after borrowing
