from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["university_db"]
students_collection = db["students"]

# Insert data into MongoDB
def insert_initial_students():
    if students_collection.count_documents({}) == 0:
        students = [
            {"name": "Anna", "email": "anna@example.com", "major": "Mathematics"},
            {"name": "Tom", "email": "tom@example.com", "major": "Computer Science"},
            {"name": "Eva", "email": "eva@example.com", "major": "Biology"}
        ]
        students_collection.insert_many(students)
        print("Inserted initial student records.")
    else:
        print("Students already exist. Skipping initial insert.")

def display_all_students():
    print("\nAll Students:")
    for student in students_collection.find():
        print(student)

# Filter students
def display_students_by_major(major):
    print(f"\nStudents majoring in {major}:")
    for student in students_collection.find({"major": major}):
        print(student)

# Update functions
def update_major_by_email(email, new_major):
    result = students_collection.update_one(
        {"email": email},
        {"$set": {"major": new_major}}
    )
    if result.modified_count > 0:
        print(f"Updated major for {email} to {new_major}")
    else:
        print("No student found with that email.")

def delete_student_by_name(name):
    result = students_collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Deleted student named {name}")
    else:
        print("No student found with that name.")


def cli_menu():
    print("\nChoose an action:")
    print("1 - Update student major")
    print("2 - Delete student")
    choice = input("Enter choice: ")

    if choice == "1":
        email = input("Enter student email: ")
        new_major = input("Enter new major: ")
        update_major_by_email(email, new_major)

    elif choice == "2":
        name = input("Enter student name to delete: ")
        delete_student_by_name(name)

    else:
        print("Invalid choice.")
    
