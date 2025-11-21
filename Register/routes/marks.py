from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from database.db import marks_collection
from auth.auth import verify_token
from models.model import Mark, MarkResponse

router = APIRouter(prefix="/marks", tags=["Marks"])

@router.post("/", response_model=MarkResponse)
def add_mark(data: Mark, username: str = Depends(verify_token)):
    new_mark = data.dict()
    result = marks_collection.insert_one(new_mark)
    new_mark["id"] = str(result.inserted_id)
    return new_mark

@router.get("/", response_model=list[MarkResponse])
def get_marks(username: str = Depends(verify_token)):
    marks = []
    for m in marks_collection.find():
        m["id"] = str(m["_id"])
        del m["_id"]
        marks.append(m)
    return marks

@router.delete("/{student}")
def delete_mark(student: str, username: str = Depends(verify_token)):
    result = marks_collection.delete_one({"student": student})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"msg": f"Mark for {student} deleted"}
