import mysql.connector
#from .config import DB_CONFIG

def get_connection():
    """Establish and return a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def init_db():
    """Create tables in the database (handled manually in MySQL directly, no ORM)."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Example query to create the users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS mysqli_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE
            );
            """)
            print("Table created successfully (if not already exists).")
        except mysql.connector.Error as err:
            print(f"Failed to create table: {err}")
        finally:
            cursor.close()
            connection.close()
