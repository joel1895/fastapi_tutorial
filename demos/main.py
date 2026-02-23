from fastapi import FastAPI,HTTPException
from models_eval import Employee
from typing import List

employee_db : List[Employee] = []
app = FastAPI()

#1. Read all employees
@app.get("/employees",response_model=List[Employee])
def get_employees():
    return employee_db

#2.Read Specific emoployee
@app.get("/employees/{emp_id}",response_model=Employee)
def get_empolyee(emp_id:int):
    for index,employee in enumerate(employee_db):
        if employee.id == emp_id:
            return employee_db[index]
    raise HTTPException(status_code=404,detail="Employee not found")

#3. Add new employee
@app.post("/add_employee",response_model=Employee)
def add_employee(new_employee:Employee):
    for employee in employee_db:
        if employee.id == new_employee.id:
            raise HTTPException(status_code=400,detail="Employee already exists")
    employee_db.append(new_employee)
    return new_employee
        
#4. Update employee
@app.put("/update_employee/{emp_id}",response_model=Employee)
def update_employee(emp_id: int, updated_employee: Employee):
    for index,empoloyee in enumerate(employee_db):
        if empoloyee.id == emp_id:
            employee_db[index] = updated_employee
            return updated_employee
    raise HTTPException(status_code=404, detail="Employee not found")

#5 .Delete an employee
@app.delete("/delete_employee/{emp_id}")
def delete_employee(emp_id:int):
    for index,employee in enumerate(employee_db):
        if employee.id == emp_id:
            del employee_db[index]
            return {"message":"Employee deleted sucessfully"}
    raise HTTPException(status_code=404,detail="Employee not found")
