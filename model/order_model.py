import sqlite3

class OrderModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.create_orders_table()  # Calling the create_orders_table method when initializing the class
        self.add_columns_if_not_exists()
        self.alter_table_for_user_id_and_title()  # Call the new method to update the schema

    def create_orders_table(self):
        """Create the orders table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                items TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                status TEXT DEFAULT 'Pending',
                note TEXT
            );
        """)
        conn.commit()
        conn.close()

    def add_columns_if_not_exists(self):
        """Add columns if they do not already exist in the table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check and add book_name column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE borrowed_books ADD COLUMN book_name TEXT;")
        except sqlite3.OperationalError:
            pass  # Column already exists, so we catch the error and do nothing

        # Check and add quantity_borrowed column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE borrowed_books ADD COLUMN quantity_borrowed INTEGER;")
        except sqlite3.OperationalError:
            pass  # Column already exists, so we catch the error and do nothing

        conn.commit()
        conn.close()

    def alter_table_for_user_id_and_title(self):
        """Ensure the `user_id` and `title` columns allow NULL values"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                ALTER TABLE borrowed_books RENAME TO old_borrowed_books;
            """)
            cursor.execute("""
                CREATE TABLE borrowed_books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,  -- Allow NULL for title
                    book_name TEXT NOT NULL,
                    quantity_borrowed INTEGER NOT NULL,
                    borrow_date DATE NOT NULL,
                    return_date DATE NOT NULL,
                    book_condition TEXT NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)
            cursor.execute("""
                INSERT INTO borrowed_books SELECT * FROM old_borrowed_books;
            """)
            cursor.execute("""
                DROP TABLE old_borrowed_books;
            """)
        except sqlite3.OperationalError:
            pass  # Handle the case where the table structure is already correct

        conn.commit()
        conn.close()

    def get_all_borrowed_books(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM borrowed_books")  # Assuming there is a table for borrowed books
        borrowed_books = cursor.fetchall()
        conn.close()
        return borrowed_books

    def get_borrowed_book_by_id(self, book_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM borrowed_books WHERE id = ?", (book_id,))
        borrowed_book = cursor.fetchone()
        conn.close()
        return borrowed_book

    def update_borrowed_book(self, book_id, book_name, quantity_borrowed, borrow_date, return_date, book_condition):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE borrowed_books
            SET book_name = ?, quantity_borrowed = ?, borrow_date = ?, return_date = ?, book_condition = ?
            WHERE id = ?
        """, (book_name, quantity_borrowed, borrow_date, return_date, book_condition, book_id))
        conn.commit()  # Commit the changes
        conn.close()
        
    def delete_borrowed_book(self, book_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM borrowed_books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()

    def create_borrowed_book(self, book_name, quantity, borrow_date, return_date, book_condition, user_id, title):
      if not title:  # Check if title is provided
        title = "Untitled Book"  # Provide a default value if title is missing
    
      with sqlite3.connect(self.db_path, timeout=10) as conn:  # Automatically handles closing the connection
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO borrowed_books (title, book_name, quantity_borrowed, borrow_date, return_date, book_condition, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, book_name, quantity, borrow_date, return_date, book_condition, user_id))
        conn.commit()  # Automatically commits changes when leaving the `with` block
