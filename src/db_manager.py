import sqlite3
import datetime

DATABASE_NAME = "users.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def init_db():
    """
    Initializes the database by creating the 'users' table if it doesn't exist.
    Optionally adds a default admin user if the table is empty.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Optional: Add a default admin user if no users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        print("No users found, adding default admin user...")
        # Importing auth_service here to avoid circular dependency at module load
        # when auth_service itself imports db_manager.
        try:
            from auth_service import hash_password
            admin_password_hash = hash_password("password123").decode('utf-8')
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, ("admin", "admin@example.com", admin_password_hash, "admin"))
            conn.commit()
            print("Default admin user created: username='admin', password='password123'")
        except ImportError:
            print("Warning: Could not import auth_service to create default admin. "
                  "Please ensure auth_service.py is present and functional.")
            conn.rollback() # Rollback if admin creation failed

    conn.close()

def add_user(username: str, email: str, password_hash: str, role: str = 'user') -> bool:
    """
    Inserts a new user record into the `users` table.

    Args:
        username (str): Unique username.
        email (str): Unique email address.
        password_hash (str): Hashed password.
        role (str, optional): User's role (e.g., 'user', 'admin'). Defaults to 'user'.

    Returns:
        bool: True if user added successfully, False otherwise (e.g., username/email already exists).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error adding user {username}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_user_by_username(username: str) -> dict | None:
    """
    Retrieves a user's details from the database based on their username.

    Args:
        username (str): The username to look up.

    Returns:
        dict: A dictionary containing user data (`id`, `username`, `email`, `password_hash`, `role`, `created_at`),
              or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

# Ensure the database is initialized when this module is imported (for initial setup)
# init_db() # This line should be called by app.py to control timing better.