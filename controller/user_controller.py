from flask import request, redirect, url_for, current_app, render_template, session, flash, jsonify
from model.user_model import UserModel  # Assuming UserModel is the class inside user_model.py
from datetime import datetime, timedelta
class UserController:
    def __init__(self):
        self.model = UserModel()

    def list_users(self):
      users = self.model.get_all_users()  # Lấy danh sách người dùng
      if users:
        user_id = users[0]['id']  # Lấy user_id của người dùng đầu tiên
      else:
        user_id = None  # Nếu không có người dùng, user_id sẽ là None

      return render_template("user_list.html", users=users, user_id=user_id)  # Truyền user_id vào template

    def get_all_borrowed_books(self, user_id):
      """
      Lấy tất cả sách mượn của người dùng từ model.
      """
      # Gọi phương thức model để lấy tất cả sách mượn cho user_id
      borrowed_books = self.model.get_all_borrowed_books(user_id)
      print(f"Borrowed books for user {user_id}: {borrowed_books}")  # Debugging line
      return borrowed_books

    def create_borrowed_book(self, user_id, title, borrow_date, return_date, status):
    # Now you can safely use these parameters to insert into the database
      self.model.create_borrowed_book(user_id, title, borrow_date, return_date, status)
      return redirect(url_for('user_borrowed_books', user_id=user_id))
    
    # Sửa phương thức user_borrowed_books trong controller
    def user_borrowed_books(self, user_id):
      borrowed_books = self.model.get_all_borrowed_books(user_id)
      books = self.model.get_available_books()  # Giả sử bạn có một phương thức này để lấy sách có sẵn để mượn
      return render_template('user_list.html', user_id=user_id, borrowed_books=borrowed_books, books=books)


    
    def delete_borrowed_book(self, user_id, book_id):
        """
        Xóa sách mượn của người dùng từ cơ sở dữ liệu.
        """
        # Gọi phương thức trong model để xóa sách mượn
        success = self.model.delete_borrowed_book(book_id)

        # Kiểm tra xem có xóa thành công không và chuyển hướng về danh sách sách mượn của người dùng
        if success:
            print(f"Book {book_id} deleted successfully for user {user_id}")
            return redirect(url_for("user_borrowed_books", user_id=user_id))
        else:
            print(f"Failed to delete book {book_id} for user {user_id}")
            return "Error deleting book", 500
        
    
    def edit_borrowed_book(self, user_id, book_id):
      """
      Chỉnh sửa thông tin sách mượn của người dùng.
      """
      book = self.model.get_borrowed_book_by_id(book_id)

      if not book:
          flash('Book not found', 'danger')
          return redirect(url_for('user_borrowed_books', user_id=user_id))

      if request.method == "POST":
          try:
              # Kiểm tra xem các trường có tồn tại trong request.form không
              if "title" not in request.form:
                raise KeyError("title")
            
              title = request.form["title"]
              borrow_date = request.form["borrow_date"]
              return_date = request.form["return_date"]
              status = request.form["status"]

              # Cập nhật thông tin sách mượn trong cơ sở dữ liệu
              self.model.update_borrowed_book(book_id, title, borrow_date, return_date, status)

              flash("Book details updated successfully!", "success")

              # Sau khi chỉnh sửa, làm mới danh sách sách mượn của người dùng
              borrowed_books = self.get_all_borrowed_books(user_id)

              return redirect(url_for("user_borrowed_books", user_id=user_id))

          except KeyError as e:
              flash(f"Missing field: {e.args[0]}", "danger")
              return redirect(url_for('edit_borrowed_book', user_id=user_id, book_id=book_id))

      return render_template("edit_borrowed_book.html", book=book, user_id=user_id)
    
    def revenue_dashboard(self):
        # Fetch the monthly revenue data
        monthly_revenue = self.model.get_monthly_revenue()
        return render_template('dashboard.html', monthly_revenue=monthly_revenue)
    
    def borrow_books(self, user_id, book_id):
        """
        Xử lý mượn sách cho người dùng.
        """
        # Lấy thông tin sách từ cơ sở dữ liệu
        book = self.model.get_book_by_id(book_id)

        if book and book['status'] == 'Available':
            borrow_date = datetime.now()
            return_date = borrow_date + timedelta(days=14)  # Ví dụ, trả sách trong 14 ngày

            # Cập nhật trạng thái sách và thêm thông tin vào bảng borrowed_books
            self.model.update_book_status(book_id, 'Borrowed')  # Cập nhật trạng thái của sách
            self.model.create_borrowed_book(user_id, book['title'], borrow_date, return_date, 'Borrowed')

            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'message': 'Book is not available'}), 400

    
   





    

