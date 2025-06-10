import pymysql
from pymysql import Error


def setup_database():
    conn = None  # Initialize conn variable
    try:
        # First connect without specifying database
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="yara1203",  # ← YOU MUST SET THIS!
            charset='utf8mb4'
        )

        with conn.cursor() as cursor:
            # Create database if not exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS pips_bluff")
            conn.commit()

            # Now connect to the specific database
            conn.select_db("pips_bluff")

            # Create users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,  # Changed from password to password_hash
                email VARCHAR(100) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

            print("✅ Database setup completed successfully.")

    except Error as err:
        print(f"❌ Error: {err}")
    finally:
        if conn:  # Now safe to check
            conn.close()


if __name__ == "__main__":
    setup_database()