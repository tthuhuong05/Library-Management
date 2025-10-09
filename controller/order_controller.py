import os
from flask import request, redirect, url_for, current_app, render_template, session
from model.order_model import OrderModel
from flask_login import current_user

class OrderController:
    def __init__(self):
        self.model = OrderModel()

    def list_borrowed_books(self):
        borrowed_books = self.model.get_all_borrowed_books()  # Assuming this method fetches borrowed books
        return render_template("borrowed_books.html", borrowed_books=borrowed_books)
    
    def edit_borrowed_book(self, book_id):
        borrowed_book = self.model.get_borrowed_book_by_id(book_id)  # Retrieve the borrowed book by ID
        
        if request.method == 'POST':  # Check if the form is being submitted
            # Get form data
            book_name = request.form['book_name']
            quantity_borrowed = int(request.form['quantity_borrowed'])
            borrow_date = request.form['borrow_date']
            return_date = request.form['return_date']
            book_condition = request.form['book_condition']

            # Call the model to update the borrowed book
            self.model.update_borrowed_book(book_id, book_name, quantity_borrowed, borrow_date, return_date, book_condition)
            
            # Redirect to the borrowed books list after saving
            return redirect(url_for('borrowed_books'))

        # If it's a GET request, just render the form to edit the book
        return render_template('edit_borrowed.html', borrowed_book=borrowed_book)
    
    def update_borrowed_book(self, book_id):
      if request.method == "POST":
        quantity_borrowed = int(request.form["quantity_borrowed"])
        borrow_date = request.form["borrow_date"]
        return_date = request.form["return_date"]
        book_condition = request.form["book_condition"]
        
        self.model.update_borrowed_book(book_id, quantity_borrowed, borrow_date, return_date, book_condition)
        return redirect(url_for("borrowed_books"))


    def delete_borrowed_book(self, book_id):
        self.model.delete_borrowed_book(book_id)
        return redirect(url_for("borrowed_books"))
    
    def create_borrowed_book(self):
      if request.method == "POST":
        book_name = request.form.get("book_name")
        quantity = int(request.form.get("quantity"))
        borrow_date = request.form.get("borrow_date")
        return_date = request.form.get("return_date")
        book_condition = request.form.get("book_condition")
        
        title = request.form.get("title")  # Retrieve the title from the form

        # Ensure title is provided, if not, set a default value
        if not title:
            title = "Untitled Book"  # Or provide a meaningful default title

        # Ensure the user is authenticated
        if current_user.is_authenticated:
            user_id = current_user.id  # Get the authenticated user's ID
        else:
            user_id = None  # Set as None if the user is not authenticated

        # Call the model method to create the borrowed book
        self.model.create_borrowed_book(book_name, quantity, borrow_date, return_date, book_condition, user_id, title)
        
        return redirect(url_for("borrowed_books"))  # Redirect to the borrowed books list
      return render_template("create_borrowed_book.html")  # Or the appropriate template you are using






 