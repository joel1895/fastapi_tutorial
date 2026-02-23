import models,schemas,crud
from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from database import engine,SessionLocal,Base
from typing import List

Base.metadata.create_all(bind=engine) #Create all database tables defined in your SQLAlchemy models, if they don’t already exist.

app = FastAPI()

#dependency with the db
def get_db():
    db = SessionLocal() #Creates new db session
    try:
        yield db
    finally:
        db.close()

#1 create employee
@app.post("/employees", response_model=schemas.EmpoloyeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session=Depends(get_db)):
    return crud.create_employee(db, employee)

#2 get all employees
@app.get("/employees", response_model=List[schemas.EmpoloyeeOut])
def get_employees(db: Session=Depends(get_db)):
    return crud.get_employees(db)

#3 get specific employee
@app.get("/employees/{emp_id}", response_model=schemas.EmpoloyeeOut)
def get_employee(emp_id: int, db: Session=Depends(get_db)):
    employee = crud.get_employee(db, emp_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found!")
    return employee

#4. Update an employees
@app.put("/employee/{emp_id}", response_model=schemas.EmpoloyeeOut)
def update_employee(employee: schemas.EmployeeUpdate, emp_id: int, db: Session=Depends(get_db)):
    db_employee = crud.update_employee(db, emp_id, employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found!")
    return db_employee

#5. Delete an employee
@app.delete("/employees/{emp_id}", response_model=dict)
def delete_employee(emp_id: int, db: Session=Depends(get_db)):
    employee = crud.delete_employee(db, emp_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found!")
    return {"Message":"Employee Successfully deleted!"}