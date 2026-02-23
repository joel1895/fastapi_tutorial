from fastapi import FastAPI
from predict import make_predictions,make_batch_predictions
from schemas import InputSchema,OutputSchema
from typing import List

app = FastAPI()

@app.get("/")
def index():
    return {"Message":"Welcome to the ML model prediction API"}

@app.post("/prediction",response_model=OutputSchema)
def predict(user_input: InputSchema):
    prediction = make_predictions(user_input.model_dump())
    return OutputSchema(predicted_price=round(prediction,2))

@app.post("/batch_prediuctions")
def batch_predict(user_inputs:List[InputSchema]):
    predictions = make_batch_predictions([x.model_dump() for x in user_inputs])
    print("predictions:",predictions)
    return [OutputSchema(predicted_price=round(prediction,2)) for prediction in predictions]
