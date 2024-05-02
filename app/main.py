from fastapi import FastAPI, Body, HTTPException, Response,Header
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr


Employee_data = [
    Employee(id=1, name='Anand', age=24, email="anand@example.com"),
    Employee(id=2, name='Sandhya', age=22, email="sandhya@example.com"),
    Employee(id=3, name='Surya', age=23, email="surya@example.com"),
]


@app.get("/employees")
async def get_all_employees():
    return Employee_data


@app.get("/employee/{id}")
async def get_employee(id: int):
    try:
        return Employee_data[id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Employee with ID {id} not found")


@app.put("/employee/{employee_id}")
async def update_employee(employee_id: int, updated_data: Employee = Body(...)):
    for i, employee in enumerate(Employee_data):
        if employee.id == employee_id:
            if employee.id != updated_data.get("id"):
                raise HTTPException(status_code=400, detail="ID cannot be updated through PUT requests")
            employee.update(updated_data)
            return {"message": "Employee updated successfully"}
    return {"message": "Employee not found"}


@app.post("/employee")
async def add_employee(new_employee: Employee = Body(...)):
    try:
        new_employee.id = max(employee.id for employee in Employee_data) + 1
        Employee_data.append(new_employee)
        return {"message": "Employee added successfully", "new_employee_id": new_employee.id}
    except ValueError: 
        raise HTTPException(status_code=422, detail="Invalid employee data")


@app.delete("/employee/{employee_id}")
async def delete_employee(employee_id: int):
    for i, employee in enumerate(Employee_data):
        if employee.id == employee_id:
            del Employee_data[i]
            return {"message": "Employee deleted successfully"}
    return {"message": "Employee not found"}


@app.patch("/employee/{employee_id}")
async def update_employee(employee_id: int, updated_data: dict[str, str]):
    employee_index = next((i for i, emp in enumerate(Employee_data) if emp.id == employee_id), None)
    if employee_index is None:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

    if not set(updated_data.keys()).issubset({"id", "name", "age", "email"}):
        raise


# #
# @app.put("/employee/{employee_id}")
# async def update_employee(employee_id: int, 
#                           updated_data: Employee = Body(...),
#                           x_auth_token: str = Header(...)):
#   for i, employee in enumerate(Employee_data):
#     if employee.id == employee_id:
#       employee.update(updated_data)  
#       return {"message": "Employee updated successfully"}
#   return {"message": "Employee not found"}

#soft delete
@app.delete("/employee/{employee_id}")
async def delete_employee(employee_id: int):
  for i, employee in enumerate(Employee_data):
    if employee.id == employee_id:
      employee.is_deleted = True
      return {"message": "Employee soft deleted successfully"}
  return {"message": "Employee not found"}
