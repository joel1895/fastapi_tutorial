from fastapi import FastAPI
from pydantic import BaseModel
from app.logic import is_eligible_for_loan



app = FastAPI()

class Applicant(BaseModel):
    income: float
    age: int
    employement_status: str

@app.post("/loan_eligibilty")
def check_eligibilty(applicant: Applicant):
    eligibilty = is_eligible_for_loan(income=applicant.income, age=applicant.age, employement_status=applicant.employement_status)
    return {'eligible': eligibilty}