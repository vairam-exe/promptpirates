import bcrypt
import db_manager
from typing import Tuple, Dict, Any

def hash_password(password: str) -> bytes:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password.

    Returns:
        bytes: The hashed password suitable for storage.
    """
    # bcrypt.gensalt() generates a salt, bcrypt.hashpw uses the salt to hash the password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain-text password matches a given hashed password.

    Args:
        plain_password (str): The plain-text password provided by the user.
        hashed_password (str): The stored hashed password (from the database).

    Returns:
        bool: True if passwords match, False otherwise.
    """
    # bcrypt.checkpw expects both inputs to be bytes
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError: # Catches errors if hashed_password is not a valid bcrypt hash
        return False

def register_user(username: str, email: str, password: str, role: str = 'user') -> Tuple[bool, str]:
    """
    Registers a new user. It hashes the password and calls db_manager.add_user.

    Args:
        username (str): New user's username.
        email (str): New user's email.
        password (str): New user's plain-text password.
        role (str, optional): User's role. Defaults to 'user'.

    Returns:
        tuple: (bool, str) where bool indicates success and str is a message.
    """
    if not username or not email or not password:
        return False, "Username, email, and password are required."
    
    # Hash the password
    hashed_pass = hash_password(password)
    
    # Add user to the database
    success = db_manager.add_user(username, email, hashed_pass.decode('utf-8'), role) # Store as UTF-8 string
    
    if success:
        return True, "Account created successfully! You can now log in."
    else:
        # db_manager handles IntegrityError for unique constraints, we just return generic error
        return False, "Registration failed. Username or email might already exist."

def authenticate_user(username: str, password: str) -> Dict[str, Any] | None:
    """
    Authenticates a user by checking credentials against the database.

    Args:
        username (str): Username provided by the user.
        password (str): Plain-text password provided by the user.

    Returns:
        dict: User dictionary (without password_hash) if authentication is successful, None otherwise.
    """
    user_data = db_manager.get_user_by_username(username)
    
    if user_data:
        # Verify the provided password against the stored hash
        if verify_password(password, user_data['password_hash']):
            # Remove password hash before returning user data
            user_data.pop('password_hash', None)
            user_data.pop('created_at', None) # Optionally remove sensitive/unnecessary info
            user_data.pop('id', None) # Optionally remove internal ID
            return user_data
    return None