
import sqlite3
import hashlib
import secrets
import hmac
from pathlib import Path

# Database location
DB_PATH = Path(__file__).resolve().parent / "edutrack.db"

# Password hashing settings
ITERATIONS = 600000


def init_db():
    """Create the database and users table."""

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                password_iterations INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def hash_password(password):
    """Convert a password into a secure salted hash."""

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    return salt.hex(), password_hash.hex()


def verify_password(password, salt, stored_hash, iterations):
    """Verify a password against its stored hash."""

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        iterations
    )

    return hmac.compare_digest(new_hash.hex(), stored_hash)


def create_user(full_name, email, password):
    """Register a new user in the database."""

    salt, password_hash = hash_password(password)

    try:
        with sqlite3.connect(DB_PATH) as connection:

            connection.execute("""
                INSERT INTO users
                (full_name, email, password_salt, password_hash,
                 password_iterations)
                VALUES (?, ?, ?, ?, ?)
            """, (
                full_name,
                email,
                salt,
                password_hash,
                ITERATIONS
            ))

        return True

    except sqlite3.IntegrityError:
        return False


def authenticate_user(email, password):
    """Check login credentials against stored database records."""

    with sqlite3.connect(DB_PATH) as connection:

        user = connection.execute("""
            SELECT id, full_name, email, password_salt,
                   password_hash, password_iterations
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

    if user is None:
        return False, None

    valid = verify_password(
        password,
        user[3],
        user[4],
        user[5]
    )

    if valid:
        user_info = {
            "id": user[0],
            "full_name": user[1],
            "email": user[2]
        }

        return True, user_info

    return False, None
