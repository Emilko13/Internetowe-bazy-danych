# TASK 1 - Simple Python MySQL Application (msql-connector-python)
---

This simple Python application connects to a MySQL database using mysql connector. 
It demonstrates basic database interaction with sql database, 
including creating tables and inserting data into them.

## Project Overview

### Features:
1. **Connect to MariaDB Database**: The application connects to a local MariaDB instance using `mysql-connector-python`.
2. **Create a Table**: A new table named `mysqli_users` is created with columns `id`, `name`, and `email`.
3. **Insert Data**: New records are inserted into the `mysqli_users` table with the `name` and `email` fields.
4. **Retrieve Data**: Fetches a user from the `mysqli_users` table and prints the details.

## Requirements

To run this project, ensure you have the following:

- **Python 3.8+** installed on your local machine.
- **MariaDB Server** running locally or on a remote machine (e.g., XAMPP).
- **venv** must be used for this task.
- **`mysql-connector-python`** package installed. You can install it using `pip`:

```bash
python -m venv venv
. .\venv\Scripts\activate  # On Windows
source venv/bin/activate   # On macOS/Linux
pip install -r requirements.txt
```

## Setup Instructions

1. Create the `app` directory with the Python file.
2. Ensure you have MariaDB running locally or set up the necessary credentials for remote connection (user is created)
3. Set up the database named `python_db` in MariaDB if it doesn't already exist:
   ```sql
   CREATE DATABASE python_db;
   ```
4. Run the Python application:
   ```bash
   python -m app
   ```

---

## Tasks

### Task 1: Implement SQL Triggers for Logging User Actions
Create a SQL trigger that automatically logs any insert, update, or delete action performed on the `mysqli_users` table into a `mysqli_logs` table.

#### Steps:
1. Create the `mysqli_logs` table:
   ```sql
   CREATE TABLE mysqli_logs (
       log_id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       action_type ENUM('INSERT', 'UPDATE', 'DELETE'),
       action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```
2. Create a trigger to store changes:
   ```sql
   CREATE TRIGGER user_changes
   AFTER INSERT OR UPDATE OR DELETE
   ON python_users
   FOR EACH ROW
   BEGIN
       INSERT INTO mysqli_logs (user_id, action_type)
       VALUES (OLD.id, 'DELETE');
   END;
   ```

### Task 2: Implement a REST API Endpoint for User Management
Extend the Python application to include a simple REST API using Flask to manage users.

#### Steps:
1. Install Flask:
   ```bash
   pip install flask
   ```
2. Create a Flask app with endpoints to:
   - Retrieve all users (`GET /users`)
   - Insert a new user (`POST /users`)
   - Delete a user (`DELETE /users/<id>`)
   - Create simple www page to manage users

### Task 3: Optimize Database Performance with Indexing
Optimize queries by adding indexes to frequently searched columns in the `mysqli_users` table.

#### Steps:
1. Identify slow queries by analyzing query performance.
2. Add an index to the `email` field for faster lookups:
   ```sql
   CREATE INDEX idx_email ON python_users(email);
   ```
3. Measure the performance improvement before and after indexing.



Submit a single ZIP file containing:

- a report on the completed task
- the source code of the program

