# TASK 2 - Simple Python SQLAlchemy MySQL Application
---

This simple Python application connects to a MySQL database using SQLAlchemy ORM. It demonstrates basic database interaction with SQLAlchemy, including creating tables and inserting data into them.

## Project Overview

### Features:
1. **Connect to MySQL Database**: The application connects to a MySQL database using SQLAlchemy and `pymysql`.
2. **Create a Table**: A new table named `sqlalchemy_users` is created with columns `id`, `name`, and `email`.
3. **Insert Data**: New records are inserted into the `sqlalchemy_users` table with the `name` and `email` fields.
4. **Retrieve Data**: Fetches a user from the `sqlalchemy_users` table and prints the details.

## Requirements

To run this project, ensure you have the following:

- **Python 3.8+** installed on your local machine.
- **MySQL** (or a MySQL-compatible database like MariaDB) running locally or on a remote machine.
- **venv** must be used for this task.
- **`SQLAlchemy`** and **`pymysql`** libraries installed. You can install them using `pip`:

```bash
python -m venv venv
. .\venv\Scripts\activate  # On Windows
source venv/bin/activate   # On macOS/Linux
pip install -r requirements.txt
```

# Setup Instructions

- Create the app directory with the Python file.
- Ensure you have MariaDB running locally or set up the necessary credentials for remote connection.
- Set up the database named python_db in MariaDB if it doesn't already exist:
```sql
CREATE DATABASE python_db;
```

```bash
python -m app
```

## Student Tasks

### Task 1: Implement an ORM Event Listener for Logging User Actions

Instead of using raw SQL triggers, use SQLAlchemy event listeners to log changes in the sqlalchemy_users table.

Steps:
- Create a logs_users table model in SQLAlchemy with id, user_id, action, and timestamp.
- Use SQLAlchemy event listeners to detect INSERT, UPDATE, and DELETE actions on sqlalchemy_users.
- Automatically insert logs into logs_users whenever changes occur.

```python 
from sqlalchemy import event
from datetime import datetime
from app import session, LogsUser, User

def log_user_changes(mapper, connection, target):
    action = "INSERT" if target.id is None else "UPDATE"
    log_entry = LogsUser(user_id=target.id, action=action, timestamp=datetime.utcnow())
    session.add(log_entry)

event.listen(User, "after_insert", log_user_changes)
event.listen(User, "after_update", log_user_changes)
```


### Task 2: Implement Transaction Handling in SQLAlchemy ORM

Enhance the application to handle transactions properly when inserting multiple users.

Steps:
- Modify the Python application to insert multiple users within a single ORM transaction.
- Ensure that if one insertion fails, the entire transaction is rolled back.
- Test by deliberately causing an error in one of the insertions.

```python 
Session = sessionmaker(bind=engine)
session = Session()

try:
    user1 = User(name="Alice", email="alice@example.com")
    user2 = User(name="Bob", email="bob@example.com")
    session.add_all([user1, user2])
    session.commit()
except Exception as e:
    session.rollback()  # Rollback transaction if an error occurs
    print("Error:", e)
finally:
    session.close()

```

### Task 3: Implement an ORM Relationship Between Users and Addresses

Extend the database model by adding an addresses table and linking it to sqlalchemy_users using a one-to-many relationship.

Steps:
- Define a new SQLAlchemy model Address with columns id, user_id, street, and city.
- Establish a one-to-many relationship between User and Address using relationship().
- Modify the application to add and query user addresses using ORM.

```python 
from sqlalchemy.orm import relationship
from app import Base

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("sqlalchemy_users.id"))
    street = Column(String(255))
    city = Column(String(255))

    user = relationship("User", back_populates="addresses")

class User(Base):
    __tablename__ = "sqlalchemy_users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    addresses = relationship("Address", back_populates="user")
```

Submit a single ZIP file containing:

- a report on the completed task
- the source code of the program
