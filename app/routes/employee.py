# from pydantic import BaseModel, EmailStr
# from fastapi import APIRouter, Depends, HTTPException, Header
# from sqlalchemy.orm import Session
# from ..database import get_db
# from .. import models

# router=APIRouter()
# class EmployeeBase(BaseModel):
#     id : int
#     names: list[str] = None  
#     emails: list[EmailStr] = None

# class EmployeeCreate(EmployeeBase):
#     id : int
#     names: list[str] 
#     emails: list[EmailStr]  

# class EmployeeUpdate(EmployeeBase):
#     id : int
#     names: list[str] = None  
#     emails: list[EmailStr] = None  

# @router.post("/employees/", headers=dict(x_token=Header(...)))
# async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
#     """Creates new employees. Consumes a list of names and emails from the body."""
#     new_employees = []
#     for name, email in zip(employee.names, employee.emails):
#         new_employee = models.Employee(name=name, email=email)
#         new_employees.append(new_employee)
#     db.add_all(new_employees)
#     db.commit()
#     return {"message": f"Created {len(new_employees)} employees"}


# @router.put("/employees/", headers=dict(x_token=Header(...)))
# async def update_employees(employee_ids: list[int], employee: EmployeeUpdate = None, db: Session = Depends(get_db)):
#     """Updates employees based on a list of IDs and optional data in the body."""
#     if not employee_ids:
#         raise HTTPException(status_code=400, detail="No employee IDs provided")

#     updated_count = 0
#     for employee_id in employee_ids:
#         existing_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
#         if not existing_employee:
#             continue  

#         if employee:  
#             if employee.names:
#                 existing_employee.name = employee.names[0]  
#             if employee.emails:
#                 existing_employee.email = employee.emails[0]  

#         db.commit()
#         updated_count += 1

#     return {"message": f"Updated {updated_count} employees"}
