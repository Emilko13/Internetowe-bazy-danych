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

 # Models for FastAPI
app = FastAPI()

class Course(BaseModel):
    title: str
    credits: int
    grade: str


class Student(BaseModel):
    name: str
    email: str
    major: str
    courses: Optional[List[Course]] = []

# Endpoints in FastAPI
@app.post("/students/")
def add_student(student: Student):
    if students_collection.find_one({"email": student.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    students_collection.insert_one(student.dict())
    return {"message": "Student added successfully"}


@app.get("/students/")
def get_all_students():
    return list(students_collection.find({}, {"_id": 0}))


@app.get("/students/{email}")
def get_student(email: str):
    student = students_collection.find_one({"email": email}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{email}")
def update_student(email: str, updated_data: Student):
    result = students_collection.update_one(
        {"email": email},
        {"$set": updated_data.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}


@app.delete("/students/{email}")
def delete_student(email: str):
    result = students_collection.delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


# Main server
if __name__ == "__main__":
    print("Running in CLI mode...\n")

    insert_initial_students()
    display_all_students()
    display_students_by_major("Computer Science")
    cli_menu()