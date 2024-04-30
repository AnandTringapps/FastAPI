from fastapi import FastAPI , Body, HTTPException

app = FastAPI()

Employee_data=[
    
    {'id': 1,'name': 'Anand', 'age': 24},
    {'id': 2,'name': 'sandhya', 'age': 22},
    {'id': 3,'name': 'surya', 'age': 23}
]

VALID_EMPLOYEE_KEYS={"id","name","age"}

@app.get("/hello")
def hello():
    return {"message": "Hello World"}

@app.get("/all")
async def get_all_employees():
    return Employee_data

@app.get("/{id}")
async def get_employee(id: int):
    return Employee_data[id-1]

@app.put("/update/{employee_id}")
async def update_employee(employee_id: int, updated_data: dict):
    for i, employee in enumerate(Employee_data):
        if employee["id"] == employee_id:
            employee.update(updated_data)
            return {"message": "Employee updated successfully"}
    return {"message": "Employee not found"}

@app.post("/insert")
async def add_employee(new_employee: dict = Body(...)):
    new_id = max(employee_id["id"] for employee_id in Employee_data) + 1
    new_employee["id"] = new_id
    Employee_data.append(new_employee)

    return {"message": "Employee added successfully", "new_employee_id": new_id}


@app.delete("/delete/{employee_id}")
async def delete_employee(employee_id: int):
    for i, employee in enumerate(Employee_data):
        if employee["id"] == employee_id:
            del Employee_data[i]  
            return {"message": "Employee deleted successfully"}
    return {"message": "Employee not found"}

@app.patch("/update_patch/{employee_id}")
async def update_employee(employee_id: int, updated_data: dict[str, str]):
    employee_index = next((i for i, emp in enumerate(Employee_data) if emp["id"] == employee_id), None)
    if employee_index is None:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

    if not set(updated_data.keys()).issubset(VALID_EMPLOYEE_KEYS):
        raise HTTPException(status_code=400, detail=f"Invalid update keys: {', '.join(set(updated_data.keys()) - VALID_EMPLOYEE_KEYS)}")

    Employee_data[employee_index].update(updated_data)
    return {"message": f"Employee with ID {employee_id} updated successfully"}

@app.head("/head")
async def head_endpoint():
    return {"message": "This is a head-only endpoint"}



