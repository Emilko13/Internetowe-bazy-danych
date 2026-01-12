import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, jsonify, render_template_string
import threading


DB_CONFIG = {
    "host": "127.0.0.1",
    "port":3306,
    "user": "root",
    "password": "admin",
    "database": "python_db"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def setup_logging_and_triggers():
    setup_statements = [
        # Create logs table if not exists
        """
        CREATE TABLE IF NOT EXISTS mysqli_logs (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            action_type ENUM('INSERT', 'UPDATE', 'DELETE'),
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        # Trigger: after insert
        """
        CREATE TRIGGER IF NOT EXISTS after_user_insert
        AFTER INSERT ON mysqli_users
        FOR EACH ROW
        BEGIN
            INSERT INTO mysqli_logs (user_id, action_type)
            VALUES (NEW.id, 'INSERT');
        END;
        """,
        # Trigger: after update
        """
        CREATE TRIGGER IF NOT EXISTS after_user_update
        AFTER UPDATE ON mysqli_users
        FOR EACH ROW
        BEGIN
            INSERT INTO mysqli_logs (user_id, action_type)
            VALUES (NEW.id, 'UPDATE');
        END;
        """,
        # Trigger: after delete
        """
        CREATE TRIGGER IF NOT EXISTS after_user_delete
        AFTER DELETE ON mysqli_users
        FOR EACH ROW
        BEGIN
            INSERT INTO mysqli_logs (user_id, action_type)
            VALUES (OLD.id, 'DELETE');
        END;
        """,
    ]

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for stmt in setup_statements:
            for result in cursor.execute(stmt, multi=True):
                pass  # execute all parts
        conn.commit()
        print("Logging table and triggers set up successfully.")
    except mysql.connector.Error as err:
        print(f"Error during setup: {err}")
    finally:
        cursor.close()
        conn.close()

def ensure_users_table():
    create_users = """
    CREATE TABLE IF NOT EXISTS mysqli_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(create_users)
        conn.commit()
        print("mysqli_users table ensured.")
    except mysql.connector.Error as err:
        print(f"Error ensuring users table: {err}")
    finally:
        cursor.close()
        conn.close()

def add_email_index():
    idx_stmt = "CREATE INDEX IF NOT EXISTS idx_email ON mysqli_users(email);"
    # MySQL doesn't support IF NOT EXISTS for CREATE INDEX in older versions.
    # Trying to create and ignore error if exists.
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE INDEX idx_email ON mysqli_users(email);")
        conn.commit()
        print("Index idx_email created on mysqli_users(email).")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_KEYNAME:
            print("Index idx_email already exists.")
        else:
            print(f"Error creating index: {err}")
    finally:
        cursor.close()
        conn.close()

app = Flask(__name__)

# Simple in-file HTML for the optional UI
HTML_PAGE = """
<!doctype html>
<html>
  <head><title>User Management</title></head>
  <body>
    <h1>User Management API (Demo UI)</h1>
    <h2>All Users</h2>
    <button onclick="fetchUsers()">Refresh</button>
    <pre id="users"></pre>

    <h2>Add User</h2>
    <form id="addForm" onsubmit="addUser(event)">
      <label>Name: <input type="text" id="name" required></label><br>
      <label>Email: <input type="email" id="email" required></label><br>
      <button type="submit">Add</button>
    </form>

    <h2>Delete User</h2>
    <form id="delForm" onsubmit="deleteUser(event)">
      <label>User ID: <input type="number" id="del_id" required></label><br>
      <button type="submit">Delete</button>
    </form>

    <script>
      async function fetchUsers(){
        const res = await fetch('/users');
        const data = await res.json();
        document.getElementById('users').textContent = JSON.stringify(data, null, 2);
      }
      async function addUser(e){
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const res = await fetch('/users', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({name, email})
        });
        const result = await res.json();
        alert(JSON.stringify(result));
        fetchUsers();
      }
      async function deleteUser(e){
        e.preventDefault();
        const id = document.getElementById('del_id').value;
        const res = await fetch('/users/' + id, { method: 'DELETE' });
        const result = await res.json();
        alert(JSON.stringify(result));
        fetchUsers();
      }
      // Load initial data
      fetchUsers();
    </script>
  </body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    return HTML_PAGE



@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name, email FROM mysqli_users;")
        rows = cursor.fetchall()
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO mysqli_users (name, email) VALUES (%s, %s);", (name, email))
        conn.commit()
        user_id = cursor.lastrowid
        return jsonify({"id": user_id, "name": name, "email": email})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM mysqli_users WHERE id = %s;", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"deleted_id": user_id})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

def run_app():
    # Ensure base tables exist before starting the server
    ensure_users_table()
    setup_logging_and_triggers()
    add_email_index()
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    # Run in a separate thread if you want to invoke setup without blocking
    run_app()