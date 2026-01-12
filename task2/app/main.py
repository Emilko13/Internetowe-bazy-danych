import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


DB_CONFIG = {
    "host": "127.0.0.1",
    "port":3306,
    "user": "root",
    "password": "admin",
    "database": "python_db"
}

DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Models for DB
class User(Base):
    __tablename__ = "sqlalchemy_users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    
    # One-to-many relationship with Address
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("sqlalchemy_users.id"), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    
    # Many-to-one relationship back to User
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return f"<Address(street='{self.street}', city='{self.city}')>"

class LogsUser(Base):
    __tablename__ = "logs_users"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(10), nullable=False)  # INSERT, UPDATE, DELETE
    timestamp = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<LogsUser(user_id={self.user_id}, action='{self.action}', timestamp={self.timestamp})>"

# ORM Event Listeners for Logging
def log_user_insert(mapper, connection, target):
    """Log INSERT operations"""
    log_entry = LogsUser(user_id=target.id, action="INSERT")
    session.add(log_entry)

def log_user_update(mapper, connection, target):
    """Log UPDATE operations"""
    log_entry = LogsUser(user_id=target.id, action="UPDATE")
    session.add(log_entry)

def log_user_delete(mapper, connection, target):
    """Log DELETE operations"""
    log_entry = LogsUser(user_id=target.id, action="DELETE")
    session.add(log_entry)

# Register event listeners
event.listen(User, "after_insert", log_user_insert)
event.listen(User, "after_update", log_user_update)
event.listen(User, "before_delete", log_user_delete)

# Utilities
def create_tables():
    """Create all tables if they don't exist"""
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def print_users_and_addresses():
    """Print all users with their addresses"""
    users = session.query(User).all()
    print("\n=== USERS AND ADDRESSES ===")
    for user in users:
        print(f"User: {user.name} ({user.email})")
        if user.addresses:
            for addr in user.addresses:
                print(f"  Address: {addr.street}, {addr.city}")
        else:
            print("  No addresses")
    print()

def print_logs():
    """Print recent log entries"""
    logs = session.query(LogsUser).order_by(LogsUser.timestamp.desc()).limit(10).all()
    print("=== RECENT LOGS ===")
    for log in logs:
        print(f"Log: user_id={log.user_id}, action={log.action}, time={log.timestamp}")
    print()

# Transactions
def insert_users_with_transaction():
    """Task 2: Insert multiple users with transaction handling"""
    print("\n=== TASK 2: TRANSACTION HANDLING ===")
    
    try:
        # Create multiple users
        user1 = User(name="Alice Smith", email="alice@example.com")
        user2 = User(name="Bob Johnson", email="bob@example.com")
        user3 = User(name="Charlie Brown", email="charlie@example.com")
        
        # Add all to session
        session.add_all([user1, user2, user3])
        session.flush()  # Flush to generate IDs for logging
        
        # Simulate an error (uncomment to test rollback)
        
        session.commit()
        print("Transaction committed: 3 users added successfully!")
        
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Transaction rolled back due to error: {e}")
    finally:
        session.close()
        session = SessionLocal()

# Relationships
def demonstrate_relationships():
    """Task 3: Demonstrate User-Address relationships"""
    print("\n=== TASK 3: USER-ADDRESS RELATIONSHIPS ===")
    
    # Find Alice and add addresses
    alice = session.query(User).filter_by(name="Alice Smith").first()
    if alice:
        addr1 = Address(street="123 Main St", city="New York")
        addr2 = Address(street="456 Oak Ave", city="Boston")
        alice.addresses.extend([addr1, addr2])
        session.commit()
        print("Added addresses to Alice")
    
    # Query Bob and print his addresses
    bob = session.query(User).filter_by(name="Bob Johnson").first()
    if bob:
        print(f"Bob's addresses: {[addr.city for addr in bob.addresses]}")
    
    print_users_and_addresses()


def main():
    """Main application entry point"""
    print("SQLAlchemy MySQL Application Starting...")
    print(f"Database: {DATABASE_URL}")
    
    try:
        
        create_tables()
        
        # Transaction handling demo
        insert_users_with_transaction()
        
        # Relationships demo
        demonstrate_relationships()
        
        # Show logs
        print_logs()
        
        # Test update logging
        user = session.query(User).filter_by(name="Alice Smith").first()
        if user:
            user.email = "alice.updated@example.com"
            session.commit()
            print("Updated Alice's email (logged automatically)")
        
        # Test delete logging
        print("\n=== TESTING DELETE LOGGING ===")
        last_user = session.query(User).order_by(User.id.desc()).first()
        if last_user:
            session.delete(last_user)
            session.commit()
            print(f"Deleted user {last_user.id} (logged automatically)")
        
        print_logs()
        
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()
        print("\nApplication completed successfully!")

if __name__ == "__main__":
    main()