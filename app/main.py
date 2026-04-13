import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load models
model = joblib.load("app/model/model.pkl")

app = FastAPI()

# Input schema (matches lab + Jenkins)
class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.get("/")
def home():
    return {"message": "Wine Quality Prediction API"}

@app.post("/predict")
def predict(data: WineInput):
    try:
        features = np.array([
            data.fixed_acidity,
            data.volatile_acidity,
            data.citric_acid,
            data.residual_sugar,
            data.chlorides,
            data.free_sulfur_dioxide,
            data.total_sulfur_dioxide,
            data.density,
            data.pH,
            data.sulphates,
            data.alcohol
        ]).reshape(1, -1)

        prediction = model.predict(features)

        return {"prediction": float(prediction[0])}

    except Exception:
        raise HTTPException(status_code=500, detail="Prediction error")