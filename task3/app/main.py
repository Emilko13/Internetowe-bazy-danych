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

