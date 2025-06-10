import pymysql
from pymysql import Error
from pymysql.cursors import DictCursor


class DBOperations:
    """A class to handle all database operations for the application."""

    def __init__(self):
        """Initializes the DBOperations class and creates a database connection."""
        self.connection = self.create_connection()

    def create_connection(self):
        """Establishes a connection to the MySQL database."""
        try:
            # Connect to the database using credentials and settings.
            # DictCursor ensures that query results are returned as dictionaries.
            return pymysql.connect(
                host="localhost",
                user="root",
                password="yara1203",
                database="pips_bluff",
                charset='utf8mb4',
                cursorclass=DictCursor
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def authenticate_user(self, username, password_hash):
        """
        Verifies a user's credentials against the database.

        Args:
            username (str): The user's username.
            password_hash (str): The user's hashed password.

        Returns:
            dict: The user's record if authentication is successful, otherwise None.
        """
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
                cursor.execute(query, (username, password_hash))
                # Fetches the first matching user record.
                return cursor.fetchone()
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None

    def register_user(self, username, email, password_hash):
        """
        Inserts a new user into the 'users' table.

        Args:
            username (str): The new user's username.
            email (str): The new user's email.
            password_hash (str): The new user's hashed password.

        Returns:
            bool: True if registration is successful, otherwise False.
        """
        try:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, email, password_hash))
                # Saves the new user record to the database.
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Registration error: {e}")
            return False

    def check_user_exists(self, username, email):
        """
        Checks if a username or email already exists in the database.

        Args:
            username (str): The username to check.
            email (str): The email to check.

        Returns:
            dict: The existing user's record if found, otherwise None.
        """
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s OR email = %s"
                cursor.execute(query, (username, email))
                return cursor.fetchone()
        except Error as e:
            print(f"Error checking user existence: {e}")
            return None

    def get_user_by_username(self, username):
        """
        Retrieves a single user's data by their username.

        Args:
            username (str): The username of the user to find.

        Returns:
            dict: The user's data if found, otherwise None.
        """
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                return cursor.fetchone()
        except Error as e:
            print(f"Error getting user: {e}")
            return None

    def change_username(self, old_username, new_username):
        """
        Updates a user's username in the database.

        Args:
            old_username (str): The current username.
            new_username (str): The new username to set.

        Returns:
            bool: True if the username was successfully changed, otherwise False.
        """
        try:
            with self.connection.cursor() as cursor:
                query = "UPDATE users SET username = %s WHERE username = %s"
                cursor.execute(query, (new_username, old_username))
                self.connection.commit()
                # Check if any rows were actually updated.
                return cursor.rowcount > 0
        except Error as e:
            print(f"Error changing username: {e}")
            # Revert the transaction if an error occurs to maintain data integrity.
            self.connection.rollback()
            return False

    def __del__(self):
        """Destructor to close the database connection when the object is destroyed."""
        if self.connection:
            self.connection.close()
