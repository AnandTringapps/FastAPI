from fastapi import APIRouter, HTTPException, Path, File, UploadFile, status, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import List
from models.books import Book, ExcelFile
from schemas.books import Response, RequestBook, BookSchema, save_uploaded_pdf
from crud import create_book, get_books, update_book, remove_book, upload_files, save_uploaded_excel, download_excel_file

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
async def create_book_service(request: RequestBook, db: Session = Depends(get_db)):
    created_book = create_book(db, book=request.parameter)
    return Response(status="Ok", code="200", message="Book created successfully", result=created_book)

@router.get("/all")
async def get_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = get_books(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=books)

@router.patch("/update")
async def update_book_endpoint(request: RequestBook, db: Session = Depends(get_db)):
    updated_book = update_book(db, book_id=request.parameter.id,
                                title=request.parameter.title, description=request.parameter.description)
    return Response(status="Ok", code="200", message="Success update data", result=updated_book)

@router.delete("/delete")
async def delete_book_endpoint(request: RequestBook, db: Session = Depends(get_db)):
    remove_book(db, book_id=request.parameter.id)
    return Response(status="Ok", code="200", message="Success delete data")


@router.post("/upload/")
async def upload_multiple_files_endpoint(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    result = await upload_files(files, db)
    return Response(status="Ok", code="200", message="Files uploaded successfully", result=result)

@router.post("/upload_excel/")
async def upload_excel_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = await save_uploaded_excel(file)
    new_excel_file = ExcelFile(filename=file.filename, file_content=file_content)
    db.add(new_excel_file)
    db.commit()
    db.refresh(new_excel_file)
    return {"detail": "Excel file uploaded successfully", "filename": new_excel_file.filename, "id": new_excel_file.id}

@router.get("/download_excel/{file_id}/")
async def download_excel_endpoint(file_id: int, db: Session = Depends(get_db)):
    return download_excel_file(file_id, db)