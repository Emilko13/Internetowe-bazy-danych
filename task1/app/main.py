import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, jsonify, render_template_string
import threading
#from database import get_connection, init_db

DB_CONFIG = {
    "host": "127.0.0.1",
    "port":3306,
    "user": "root",
    "password": "admin",
    "database": "python_db"
}


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


def create_user(db, name: str, email: str):
    """Create a new user"""
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO mysqli_users (name, email) VALUES (%s, %s)", (name, email)
        )
        db.commit()  # Commit the transaction
        # Get the ID of the last inserted user
        user_id = cursor.lastrowid
        cursor.close()
        
        # Return user details (simulated as a dictionary)
        return {"id": user_id, "name": name, "email": email}
    except mysql.connector.Error as err:
        print(f"Error creating user: {err}")
        return None

def get_user(db, user_id: int):
    """Get user by ID"""
    try:
        cursor = db.cursor(dictionary=True)  # Using dictionary to return data as a dictionary
        cursor.execute("SELECT id, name, email FROM mysqli_users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
    except mysql.connector.Error as err:
        print(f"Error retrieving user: {err}")
        return None

def main():
    """Main function to run the app"""
    # Initialize DB (create tables)
    init_db()

    # Open a connection to interact with the database
    db = get_connection()
    if db is None:
        print("Failed to connect to the database.")
        return

    # Create a new user
    new_user = create_user(db, name="John Doe", email="johndoe@example.com")
    if new_user:
        print(f"User created: {new_user['name']} ({new_user['email']})")

    # Get the user back
    user = get_user(db, new_user['id'])
    if user:
        print(f"Retrieved user: {user['name']} ({user['email']})")

    # Close the connection
    db.close()

if __name__ == "__main__":
    main()
