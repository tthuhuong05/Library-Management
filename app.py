from flask import Flask, render_template, request, session, redirect, url_for, current_app, flash, jsonify
from controller.book_controller import BookController
from controller.user_controller import UserController  # Import UserController
import os

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_IN_PRODUCTION"

book_controller = BookController()  # Global instance for BookController
user_controller = UserController()  # Global instance for UserController

# Route for the main library page
@app.route("/")
def library():
    books = book_controller.get_books()  # Fetch books from the controller
    return render_template('library.html', books=books)  # Pass books to the template

# Route to show book list
@app.route("/library")
def show_book_list():
    return book_controller.request_books()  # Directly use the controller's method

# Route to create a new book
@app.route("/library/create")
def create_book():
    return book_controller.create_book()

# Route to store a new book
@app.route("/library/store", methods=["POST"])
def store_book():
    status = request.form.get("status", "Available")  # Default to "Available" if not provided
    return book_controller.store_book(status=status)

# Route to edit a specific book
@app.route("/library/edit/<int:book_id>", methods=['GET', 'POST'])
def edit_book(book_id):
    book_item = book_controller.get_book_by_id(book_id)  # Get the current book info

    if not book_item:
        return "Book not found", 404

    if request.method == 'POST':
        # Get data from form
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        year = request.form['year']
        status = request.form['status']  # Ensure status is retrieved correctly from form

        image_file = request.files.get('image')
        image_filename = None

        if image_file and image_file.filename != "":
            image_filename = image_file.filename
            upload_path = os.path.join(current_app.root_path, 'static', 'uploads', image_filename)
            image_file.save(upload_path)

        # Update the book details
        if book_controller.update_book(book_id, title, author, publisher, year, status, image_filename):
            return redirect(url_for('show_book_list'))  # Redirect to the book list after update
        else:
            return "Error updating book", 500

    return render_template("edit_book.html", book=book_item)

# Route to delete a book
@app.route("/library/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    return book_controller.delete_book(book_id)

# Route to search books
@app.route("/library/search")
def search():
    query = request.args.get('query')  # Get the search query from the URL
    if query:
        items = book_controller.search_books(query)  # Perform the search using BookController
    else:
        items = []  # Return an empty list if no query is provided
    return render_template('search_books.html', items=items)


    


# Route to show the list of users
@app.route("/user")
def user_list():
    user_controller = UserController()
    return user_controller.list_users()


@app.route('/create_borrowed_book/<int:user_id>', methods=['GET', 'POST'])
def create_borrowed_book(user_id):
   
    if request.method == 'POST':
        title = request.form.get('title')
        borrow_date = request.form.get('borrow_date')
        return_date = request.form.get('return_date')
        status = request.form.get('status')

        if title and borrow_date and return_date and status:
            # Pass the correct arguments to create_borrowed_book method in the controller
            user_controller.create_borrowed_book(user_id, title, borrow_date, return_date, status)
            flash('Book borrowed successfully!', 'success')
            return redirect(url_for('user_borrowed_books', user_id=user_id))
        else:
            flash('All fields are required!', 'danger')
            return render_template('create_borrowed_book.html', user_id=user_id)

    return render_template('borrowed_book.html', user_id=user_id)  # For GET request, render the form



# Route to return a book
@app.route("/return_book/<int:book_id>", methods=["POST", "GET"])
def return_book(book_id):
    user_controller.model.return_book(book_id)  # Mark the book as returned
    flash("Book returned successfully!", "success")
    return redirect(url_for("library"))  # Redirect to the library page

@app.route('/user/<int:user_id>/borrowed_books')
def user_borrowed_books(user_id):
    borrowed_books = user_controller.get_all_borrowed_books(user_id)  # Fetch borrowed books
    return render_template('user_list.html', borrowed_books=borrowed_books)



@app.route("/user/<int:user_id>/delete_borrowed_book/<int:book_id>", methods=["POST"])
def delete_borrowed_book(user_id, book_id):
    # Gọi phương thức trong controller để xóa sách mượn
    user_controller.delete_borrowed_book(user_id, book_id)

    flash("Book successfully removed from borrowed list!", "success")
    return redirect(url_for('user_borrowed_books', user_id=user_id))

@app.route("/user/<int:user_id>/edit_borrowed_book/<int:book_id>", methods=["GET", "POST"])
def edit_borrowed_book(user_id, book_id):
    return user_controller.edit_borrowed_book(user_id, book_id)

@app.route("/dashboard")
def dashboard():
    return user_controller.revenue_dashboard()


@app.route("/borrow_book/<int:user_id>/<int:book_id>", methods=["POST"])
def borrow_books(user_id, book_id):
    success = user_controller.borrow_books(user_id, book_id)
    if success:
        return redirect(url_for('user_borrowed_books', user_id=user_id))  # Redirect after successful borrow
    else:
        flash('Error borrowing book', 'danger')
        return redirect(url_for('library'))  # Or handle error


@app.route("/borrow_book/<int:book_id>", methods=["POST"])
def borrow_book(book_id):
    user_id = session.get('user_id')  # Assuming user_id is stored in the session after login
    if not user_id:
        flash('You must be logged in to borrow a book', 'danger')
        return redirect(url_for('login'))  # Redirect if the user is not logged in

    # Get book details from the database
    book = book_controller.get_book_by_id(book_id)
    if book and book['status'] == 'Available':
        # Change book status to 'Borrowed'
        book_controller.update_book_status(book_id, 'Borrowed')
        
        # Add to borrowed_books table
        borrow_date = '2025-02-20'  # Sample borrow date
        return_date = '2025-03-20'  # Sample return date
        status = 'Borrowed'
        
        # Insert the book info into the borrowed_books table
        user_controller.create_borrowed_book(user_id, book['title'], borrow_date, return_date, status)

        # Prepare book details as a dictionary
        book_details = {
            'id': book_id,
            'title': book['title'],
            'borrow_date': borrow_date,
            'return_date': return_date,
            'status': status
        }

        # Add the book information as a JSON string into the user_list table
        user_controller.add_borrowed_book_to_user_list(user_id, book_details)

        # Return success response with book details
        response = {
            'success': True,
            'message': 'Book borrowed successfully!',
            'book': book_details
        }

        return jsonify(response)
    else:
        flash('This book is not available for borrowing', 'danger')
        return jsonify({'success': False, 'message': 'Book not available'}), 400



@app.route("/library/delete_available_book/<int:book_id>", methods=["POST"])
def delete_available_book(book_id):
    # Delete the book from the available books list
    success = book_controller.delete_book(book_id)  # Modify this to delete the book as needed
    if success:
        flash("Book removed from available list!", "success")
        return redirect(url_for('library'))  # Redirect to library page or wherever you want
    else:
        flash("Failed to remove the book", "danger")
        return redirect(url_for('library'))


if __name__ == "__main__":
    app.run(debug=True)
