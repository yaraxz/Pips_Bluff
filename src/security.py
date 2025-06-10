import bcrypt
import hashlib


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt (preferred) or SHA-256 as a fallback.

    bcrypt is used for secure password hashing with built-in salting.
    If bcrypt is unavailable or fails, fallback to SHA-256 for compatibility.
    """
    try:
        # Generate a salt and hash the password with bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    except Exception:
        # If bcrypt fails, fallback to SHA-256 (less secure, no salting)
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored hash.

    Tries bcrypt verification first. If it fails (e.g., hash is from SHA-256),
    it falls back to comparing the SHA-256 hash of the input.
    """
    try:
        # Attempt bcrypt verification (assumes hashed_password is a bcrypt hash)
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    except ValueError:
        # Fallback to SHA-256 comparison if bcrypt fails (e.g., hash format mismatch)
        return hashlib.sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password
