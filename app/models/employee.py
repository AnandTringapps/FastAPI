# from pydantic import BaseModel, EmailStr, validator
# from sqlalchemy import Boolean, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Employee(Base):
#     __tablename__ = "employees"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, index=True, unique=True)
#     is_deleted = Column(Boolean, default=False)

# class EmployeeBase(BaseModel):
#     id: int  
#     name: str
#     email: EmailStr

# class EmployeeCreate(EmployeeBase):
#     pass

# class EmployeeUpdate(EmployeeBase):
#     pass

# class EmployeeInDB(EmployeeBase):
#     id: int
#     is_deleted = bool

#     class Config:
#         orm_mode = True
