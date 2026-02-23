from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_eligibilty_pass():
    payload = {
        "income" : 60000,
        "age" : 25,
        "employement_status" : "employed"
    }

    response = client.post("/loan_eligibilty", json=payload)
    assert response.status_code == 200
    assert response.json() == {'eligible' : True}

def test_eligiblty_fail():
    payload = {
        "income": 30000,
        "age" : 18,
        "employement_status" : "unemployed"
    }

    response = client.post("/loan_eligibilty", json=payload)
    assert response.status_code == 200
    assert response.json() == {'eligible': False}