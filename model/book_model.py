import sqlite3

class BookModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.create_books_table()

    def create_books_table(self):
        """Create the 'books' table with the 'status' column."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT NOT NULL,
                year INTEGER NOT NULL,
                image TEXT,
                status TEXT DEFAULT 'Available'  -- Adding status column with default value
            )
        """)
        connection.commit()
        connection.close()

    def store_book(self, title, author, publisher, year, status, image_filename=None):
        """Insert a new book into the 'books' table."""
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO books (title, author, publisher, year, image, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, author, publisher, year, image_filename, status))
            connection.commit()
            connection.close()
            print("Book inserted successfully.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
            connection.close()

    def get_books(self):
        """Fetch all books from the 'books' table."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, author, publisher, year, image, status FROM books")
        results = cursor.fetchall()
        connection.close()
        books = []
        for row in results:
            item_id, title, author, publisher, year, image, status = row
            books.append({
                "id": item_id,
                "title": title,
                "author": author,
                "publisher": publisher,
                "year": year,
                "image": image,
                "status": status  # Add status here
            })
        return books

    def update_book(self, book_id, title, author, publisher, year, status, image_filename=None):
        """Update the details of an existing book."""
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE books
                SET title = ?, author = ?, publisher = ?, year = ?, image = ?, status = ?
                WHERE id = ?
            """, (title, author, publisher, year, image_filename, status, book_id))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            connection.close()
            return False

    def delete_book(self, book_id):
        """Delete a book from the 'books' table."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        connection.commit()
        connection.close()

    def get_book_by_id(self, book_id):
        """Fetch a single book's details based on its ID."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, title, author, publisher, year, image, status
            FROM books WHERE id = ?
        """, (book_id,))
        result = cursor.fetchone()
        connection.close()
        if result:
            item_id, title, author, publisher, year, image, status = result
            return {
                "id": item_id,
                "title": title,
                "author": author,
                "publisher": publisher,
                "year": year,
                "image": image,
                "status": status  # Include status
            }
        return None

    def search_books(self, keyword):
        """Search for books based on keyword."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        query = "SELECT id, title, author, publisher, year, image, status FROM books WHERE title LIKE ? OR author LIKE ?"
        params = (f"%{keyword}%", f"%{keyword}%")
        cursor.execute(query, params)
        results = cursor.fetchall()
        connection.close()
        books = []
        for row in results:
            item_id, title, author, publisher, year, image, status = row
            books.append({
                "id": item_id,
                "title": title,
                "author": author,
                "publisher": publisher,
                "year": year,
                "image": image,
                "status": status  # Include status
            })
        return books
