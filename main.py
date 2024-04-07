from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb+srv://sumit07:Sumit6200584775@cluster0.pve845i.mongodb.net/")
db = client["students_db"]
collection = db["students"]


# Pydantic model for Student
class Student(BaseModel):
    name: str
    age: int
    address: dict


# Endpoint to create a new student record
@app.post("/students", response_model=dict, status_code=201)
async def create_student(student: Student):
    result = collection.insert_one(student.dict())
    return {"id": str(result.inserted_id)}


# Endpoint to retrieve a list of student records
@app.get("/students", response_model=list)
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = list(collection.find(query, {"_id": 0}))
    return students


# Endpoint to retrieve a specific student record by ID
@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = collection.find_one({"_id": ObjectId(student_id)})
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@app.patch("/students/{student_id}", response_model=dict)
async def update_student(student_id: str, student: Student):
    result = collection.update_one({"_id": ObjectId(student_id)}, {"$set": student.dict()})
    if result.modified_count == 1:
        return {"message": "Student updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/students/{student_id}", response_model=dict)
async def delete_student(student_id: str):
    result = collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 1:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")