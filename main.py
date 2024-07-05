from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()  # Create an instance of the FastAPI class

students = {
    1: {
        "name": "John",
        "age": 17,
        "year": "Year 12",
    }
}


class Student(BaseModel):
    name: str = Field(..., example="Hello World")
    age: int = Field(..., example=99)
    year: str = Field(..., example="Year 99")


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


class DeleteStudent(BaseModel):
    student_id: int = Field(..., example=1)


@app.get("/")
def index():
    return {"name": 'First FastAPI App'}


@app.get("/get-student/{student_id}")
def get_student_by_id(student_id: int = Path(description="The ID of the student you want to view", gt=0)):
    if student_id not in students:
        return {"Error": "Student not found"}
    return students[student_id]


@app.get('/get-by-name')
def get_student_by_name(name: Optional[str] = None):
    for student_id, student_info in students.items():
        if student_info['name'] == name:
            return student_info
    return {"Data": "Not found"}


@app.post("/create_student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id] = student.dict()
    return students[student_id]


@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    student_data = students[student_id]
    if student.name is not None:
        student_data['name'] = student.name
    if student.age is not None:
        student_data['age'] = student.age
    if student.year is not None:
        student_data['year'] = student.year
    return student_data


@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int = Path(description="The ID of the student to delete", gt=0)):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}

