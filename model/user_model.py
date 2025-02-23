import sqlite3
import json
class UserModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self._create_tables()
        self.create_sales_table()
        

    def _create_tables(self):
        """Create the necessary tables in the database if they don't exist."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Create 'users' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # Create 'borrowed_books' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrowed_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                borrow_date DATE NOT NULL,
                return_date DATE NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.commit()
        connection.close()

    def create_borrowed_book(self, user_id, title, borrow_date, return_date, status):
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
      cursor.execute("""
        INSERT INTO borrowed_books (user_id, title, borrow_date, return_date, status)
        VALUES (?, ?, ?, ?, ?)
      """, (user_id, title, borrow_date, return_date, status))
      connection.commit()
      connection.close()

      print(f"Inserted borrowed book for user {user_id} with title {title}")  # Debugging line



    def get_all_borrowed_books(self, user_id):
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
      cursor.execute("""
        SELECT id, title, borrow_date, return_date, status
        FROM borrowed_books WHERE user_id = ?
      """, (user_id,))
      results = cursor.fetchall()
      print(f"Fetched books from DB: {results}")  # Kiểm tra kết quả trả về
      connection.close()

      borrowed_books = [{'id': book[0], 'title': book[1], 'borrow_date': book[2], 'return_date': book[3], 'status': book[4]} for book in results]
      return borrowed_books



    

    def get_all_users(self):
      """Get all users who have borrowed books."""
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
    
      # Get distinct user_ids from borrowed_books table
      cursor.execute("SELECT DISTINCT user_id FROM borrowed_books")
      user_ids = cursor.fetchall()
    
      # For each user_id, you can fetch the books they borrowed
      users = []
      for user_id in user_ids:
        user_books = self.get_all_borrowed_books(user_id[0])  # Fetch borrowed books for the user
        users.append({
            'id': user_id[0],
            'borrowed_books': user_books  # List of borrowed books for that user
        })

      connection.close()
      return users




    def return_book(self, book_id):
        """Mark a book as returned in the database."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE borrowed_books SET status = 'Returned' WHERE id = ?
        """, (book_id,))
        connection.commit()
        connection.close()

    def delete_borrowed_book(self, book_id):
      """Xóa sách mượn khỏi cơ sở dữ liệu."""
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
      cursor.execute("DELETE FROM borrowed_books WHERE id = ?", (book_id,))
      connection.commit()
      connection.close()
      return True
    
    def get_borrowed_book_by_id(self, book_id):
        """
        Lấy thông tin sách mượn theo ID từ cơ sở dữ liệu.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, title, borrow_date, return_date, status
            FROM borrowed_books
            WHERE id = ?
        """, (book_id,))
        
        result = cursor.fetchone()
        connection.close()

        if result:
            return {
                'id': result[0],
                'title': result[1],
                'borrow_date': result[2],
                'return_date': result[3],
                'status': result[4]
            }
        return None  # Nếu không tìm thấy sách, trả về None
    
    def update_borrowed_book(self, book_id, title, borrow_date, return_date, status):
        """
        Cập nhật thông tin sách mượn trong cơ sở dữ liệu.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE borrowed_books
            SET title = ?, borrow_date = ?, return_date = ?, status = ?
            WHERE id = ?
        """, (title, borrow_date, return_date, status, book_id))

        connection.commit()
        connection.close()
      
    def insert_sample_sales_data(self):
        """Insert sample sales data into the sales table."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Insert sample sales data
        cursor.execute("INSERT INTO sales (sale_date, amount) VALUES ('2025-01-01', 500)")
        cursor.execute("INSERT INTO sales (sale_date, amount) VALUES ('2025-01-15', 300)")
        cursor.execute("INSERT INTO sales (sale_date, amount) VALUES ('2025-02-01', 700)")

        connection.commit()
        connection.close()
    
    def get_monthly_revenue(self):
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
    
      # Query to get monthly revenue data
      cursor.execute("""
        SELECT strftime('%Y-%m', sale_date) AS month, SUM(amount) AS total_revenue
        FROM sales
        GROUP BY month
        ORDER BY month DESC
      """)
      results = cursor.fetchall()
      connection.close()
    
      print(f"Monthly revenue fetched: {results}")  # Debugging line

      monthly_revenue = [{'month': result[0], 'total_revenue': result[1]} for result in results]
      return monthly_revenue

    
    def create_sales_table(self):
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()

      # Create 'sales' table
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date DATE NOT NULL,
            amount REAL NOT NULL
        )
      """)
      connection.commit()
      connection.close()

    def get_book_by_id(self, book_id):
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
      cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
      result = cursor.fetchone()
      connection.close()
    
      if result:
        return {
            'id': result[0],
            'title': result[1],
            'author': result[2],
            'publisher': result[3],
            'year': result[4],
            'status': result[5]
        }
      return None  # Nếu không tìm thấy sách, trả về None

    
    def get_available_books(self):
      """Lấy danh sách sách có sẵn để mượn từ cơ sở dữ liệu."""
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
      cursor.execute("""
        SELECT id, title, status FROM books WHERE status = 'Available'
      """)
      results = cursor.fetchall()
      connection.close()

      # Chuyển kết quả thành danh sách các sách
      available_books = [{'id': book[0], 'title': book[1], 'description': book[2]} for book in results]
      return available_books

    def update_book_status(self, book_id, status):
        """Cập nhật trạng thái của sách."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE books SET status = ? WHERE id = ?
        """, (status, book_id))
        connection.commit()
        connection.close()
    
    def delete_available_book(self, book_id):
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
      cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
      connection.commit()
      connection.close()
      print(f"Book with ID {book_id} deleted.")  # Debugging line
      return True
    
    def add_borrowed_book_to_user_list(self, user_id, book_details):
        """Add the borrowed book details as a JSON string in the user_list."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Convert the book details to a JSON string
        book_details_json = json.dumps(book_details)

        # Insert the JSON data into user_list
        cursor.execute("""
            INSERT INTO user_list (user_id, book_details)
            VALUES (?, ?)
        """, (user_id, book_details_json))
        
        connection.commit()
        connection.close()

    
    
