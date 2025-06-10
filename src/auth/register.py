from database.db_operations import DBOperations
from security import hash_password
import logging


# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Register:
    def __init__(self):
        # Initialize database operation instance
        self.db = DBOperations()
        logger.debug("Registration handler initialized")

    def register(self, username, email, password, confirm_password):
        try:
            logger.debug(f"Registration attempt for: {username}")

            # Validate all required fields are filled
            if not all([username, email, password, confirm_password]):
                logger.warning("Missing required fields")
                return False, "All fields are required"

            # Check if both passwords match
            if password != confirm_password:
                logger.warning("Password confirmation mismatch")
                return False, "Passwords do not match"

            # Check if the user already exists in the database
            if self.db.check_user_exists(username, email):
                logger.warning(f"User already exists: {username}")
                return False, "Username or email already exists"

            # Hash the password before storing it
            hashed_password = hash_password(password)
            logger.debug(f"Generated hash: {hashed_password[:20]}...")  # Partial hash for logging

            # Insert the user into the database
            if self.db.register_user(username, email, hashed_password):
                logger.info(f"Successfully registered user: {username}")
                return True, "Registration successful"

            # If DB operation failed for unknown reasons
            logger.error("Registration failed in database operation")
            return False, "Registration failed"

        except Exception as e:
            # Catch unexpected errors and log them
            logger.error(f"Registration error: {str(e)}")
            return False, "An error occurred during registration"