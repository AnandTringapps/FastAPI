from sqlalchemy import  Column, Integer, String, LargeBinary
from database import Base
from pydantic import BaseModel
from typing import Optional

# class Book(Base):
#     __tablename__ ="Book"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     description = Column(String)
#     file_path = Column(LargeBinary)

class FileMetadata(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_path = Column(String)

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_content = Column(LargeBinary)

class ExcelFile(Base):
    __tablename__ = 'excel_files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_content = Column(LargeBinary)