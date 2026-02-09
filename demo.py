from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Model dữ liệu sinh viên
class Student(BaseModel):
    id: int
    name: str
    age: int
    email: str

# Model dùng cho PATCH (cập nhật 1 phần)
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None

# "Database giả" (lưu trong RAM)
students: List[Student] = []

# =========================
# 1. GET - Lấy tất cả sinh viên
# =========================
@app.get("/students")
def get_students():
    return students

# =========================
# 2. POST - Thêm sinh viên mới
# =========================
@app.post("/students")
def create_student(student: Student):
    students.append(student)
    return {"message": "Student added", "data": student}

# =========================
# 3. PUT - Cập nhật toàn bộ sinh viên theo id
# =========================
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == student_id:
            students[index] = updated_student
            return {"message": "Student updated", "data": updated_student}
    return {"error": "Student not found"}

# =========================
# 4. PATCH - Cập nhật một phần
# =========================
@app.patch("/students/{student_id}")
def patch_student(student_id: int, updated_data: UpdateStudent):
    for student in students:
        if student.id == student_id:
            if updated_data.name is not None:
                student.name = updated_data.name
            if updated_data.age is not None:
                student.age = updated_data.age
            if updated_data.email is not None:
                student.email = updated_data.email
            return {"message": "Student partially updated", "data": student}
    return {"error": "Student not found"}

# =========================
# 5. DELETE - Xóa sinh viên
# =========================
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student.id == student_id:
            deleted_student = students.pop(index)
            return {"message": "Student deleted", "data": deleted_student}
    return {"error": "Student not found"}
