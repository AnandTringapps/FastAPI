from sqlalchemy.orm import Session
from models.books import Book, ExcelFile
from fastapi import FastAPI, UploadFile, HTTPException,Response
from database import DATABASE_URL
import pandas as pd
from schemas.books import BookSchema
from typing import List

def get_book(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book: BookSchema):
    _book = Book(title=book.title, description=book.description)
    db.add(_book)
    db.commit()
    db.refresh(_book)
    return _book


def remove_book(db: Session, book_id: int):
    _book = get_book_by_id(db=db, book_id=book_id)
    db.delete(_book)
    db.commit()


def update_book(db: Session, book_id: int, title: str, description: str):
    _book = get_book_by_id(db=db, book_id=book_id)

    _book.title = title
    _book.description = description

    db.commit()
    db.refresh(_book)
    return _book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()


async def upload_files(files: List[UploadFile], db: Session):
    if not db:
        raise HTTPException(status_code=500, detail="Database session not available")

    uploaded_count = 0
    responses = []

    for uploaded_file in files:
        try:
            if uploaded_file.filename.endswith('.pdf'):
                file_content = await uploaded_file.read()
                new_book = Book(filename=uploaded_file.filename, file_content=file_content)

                db.add(new_book)
                db.commit()
                db.refresh(new_book)
                uploaded_count += 1

                responses.append({"filename": new_book.filename, "id": new_book.id})
        except Exception as e:
            print(f"Error uploading file: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    if uploaded_count == 0:
        raise HTTPException(status_code=400, detail="No PDF files uploaded successfully")

    return {"detail": f"{uploaded_count} PDF files uploaded successfully.", "data": responses}
async def upload_excel_data(file_path: str, db: Session = None):
    if not db:
        raise HTTPException(status_code=500, detail="Database session not available")
    try:
        df = pd.read_excel(file_path) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Excel file: {e}")

    for index, row in df.iterrows():
        book_data = {
            "title": row["Title"], 
            "description": row["Description"]  
        }
        new_book = Book(**book_data)
        db.add(new_book)
    
    try:
        db.commit()
        return {"message": "Excel data uploaded successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error committing data to the database: {e}")
    
async def save_uploaded_excel(file: UploadFile) -> bytes:
    file_content = await file.read()
    return file_content
def download_excel_file(file_id: int, db: Session) -> Response:
    excel_file = db.query(ExcelFile).filter(ExcelFile.id == file_id).first()
    if not excel_file:
        raise HTTPException(status_code=404, detail="Excel file not found")

    response = Response(content=excel_file.file_content)
    response.headers["Content-Disposition"] = f"attachment; filename={excel_file.filename}"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response