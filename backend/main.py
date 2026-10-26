from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import text

from database import engine


# Load the trained pipe-condition model once at startup.
MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "leaklytex_pipe_condition_model.joblib"
)

model = joblib.load(MODEL_PATH)


app = FastAPI(
    title="LeaklyTex API",
    description="AI-Based Wastewater Pipeline Health and Predictive Maintenance System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



class PipeConditionInput(BaseModel):
    region: str = Field(min_length=1)
    diameter_mm: float = Field(gt=0)
    material: str = Field(min_length=1)
    age_years: float = Field(ge=0)
    length_m: float = Field(gt=0)


@app.get("/")
def root():
    return {
        "project": "LeaklyTex",
        "message": "LeaklyTex Backend is running",
        "status": "OK"
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }


@app.post("/predict/pipe-condition")
def predict_pipe_condition(data: PipeConditionInput):
    input_data = pd.DataFrame([{
        "region": data.region,
        "diameter_mm": data.diameter_mm,
        "material": data.material,
        "age_years": data.age_years,
        "length_m": data.length_m
    }])

    try:
        predicted_condition = str(model.predict(input_data)[0])
        probabilities = model.predict_proba(input_data)[0]

        class_probabilities = {
            str(label): round(float(probability), 4)
            for label, probability in zip(model.classes_, probabilities)
        }

        return {
            "predicted_condition": predicted_condition,
            "class_probabilities": class_probabilities,
            "model_version": "1.0.0",
            "note": "This predicts pipe condition; it does not confirm a leak."
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Pipe-condition prediction failed."
        )
