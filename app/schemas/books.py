from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from fastapi import UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from models.books import Book
import shutil
import os
from pydantic.generics import GenericModel

T = TypeVar('T')


class BookSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestBook(BaseModel):
    parameter: BookSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

def save_uploaded_file(file: UploadFile) -> str:
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:  
        shutil.copyfileobj(file.file, buffer)
    return file_path


async def create_upload_pdf(file: UploadFile, db: Session = None):
    if not db:
        raise HTTPException(status_code=500, detail="Database session not available")

    file_path = save_uploaded_file(file)

    new_book = Book(file_path=file_path) 

    db.add(new_book)
    db.commit()

    return {"filename": file.filename}


async def upload_files(files: List[UploadFile] = File(...), db: Session = None):
    if not db:
        raise HTTPException(status_code=500, detail="Database session not available")

    uploaded_count = 0
    responses = []

    for uploaded_file in files:
        try:
            file_path = save_uploaded_file(uploaded_file)
            new_book = Book(filename=uploaded_file.filename, file_path=file_path)

            db.add(new_book)
            db.commit()
            db.refresh(new_book)
            uploaded_count += 1

            responses.append({"filename": new_book.filename, "id": new_book.id})
        except Exception as e:
            print(f"Error uploading file: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    if uploaded_count == 0:
        raise HTTPException(status_code=400, detail="No files uploaded successfully")

    return {"detail": f"{uploaded_count} files uploaded successfully.", "data": responses}

async def save_uploaded_pdf(file: UploadFile) -> bytes:
    file_content = await file.read()
    return file_content
