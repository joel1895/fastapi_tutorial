import redis
import json
import hashlib
import joblib
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

model = joblib.load("/Users/joeljacob/Desktop/joel/fastapi_course/Performance Optimization and Montoring/ml-caching/model.joblib")

class IrisFlower(BaseModel):
    SepalLengthcm: float
    SepalWidthcm: float
    PetalLengthcm: float
    PetalWidthcm: float

    def to_list(self):
        return [
            self.SepalLengthcm,
            self.SepalWidthcm,
            self.PetalLengthcm,
            self.PetalWidthcm
        ]
    
    def cache_key(self):
        raw = json.dumps(self.model_dump(), sort_keys=True)
        print("SELF DUMP: ",self.model_dump()," ",type(self.model_dump()))
        print("RAW: ",raw," ",type(raw))
        return f"Predict: {hashlib.sha256(raw.encode()).hexdigest()}"

@app.post("/predict")
async def predict(data: IrisFlower):
    key = data.cache_key()
    print("KEY: ",key)

    cached_result = redis_client.get(key) #checking if data exists in cache
    if cached_result:
        print("Serving prediction from Cache!")
        return json.loads(cached_result)
    
    print("DATA: ",data)
    print("Data to list: ",data.to_list())
    prediction = model.predict([data.to_list()])[0]
    result = {"prediction": int(prediction)}
    redis_client.set(key, json.dumps(result), ex=3600)
    return result

