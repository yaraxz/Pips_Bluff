import bcrypt
import hashlib

def hash_password(password: str) -> str:
    """Hash a password using bcrypt (preferred) or SHA-256 as fallback"""
    try:
        # Using bcrypt (more secure)
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    except Exception:
        # Fallback to SHA-256 if bcrypt fails
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        # Try bcrypt first
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        # Fallback to SHA-256 verification
        return hashlib.sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password