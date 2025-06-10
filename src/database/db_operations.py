import pymysql
from pymysql import Error


class DBOperations:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            return pymysql.connect(
                host="localhost",
                user="root",
                password="yara1203",
                database="pips_bluff",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def authenticate_user(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                return cursor.fetchone()
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None

    def register_user(self, username, email, password_hash):  # Renamed parameter for clarity
        try:
            with self.connection.cursor() as cursor:
                query = """INSERT INTO users 
                          (username, email, password_hash) 
                          VALUES (%s, %s, %s)"""
                cursor.execute(query, (username, email, password_hash))
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Registration error: {e}")
            return False

    def check_user_exists(self, username, email):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s OR email = %s"
                cursor.execute(query, (username, email))
                return cursor.fetchone()
        except Error as e:
            print(f"Error checking user existence: {e}")
            return None

    def __del__(self):
        if self.connection:
            self.connection.close()

    def get_user_by_username(self, username):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                return cursor.fetchone()  # Returns None if user not found
        except Error as e:
            print(f"Error getting user: {e}")
            return None