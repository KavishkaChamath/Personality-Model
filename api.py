"""
Personality Predictor API
--------------------------
FastAPI service that wraps the trained SVM model + label encoders and
exposes a public POST endpoint for introvert/extrovert prediction.

Run locally:
    uvicorn api:app --reload --port 8000

Endpoints:
    GET  /         -> health/status check
    GET  /health   -> health check
    POST /predict  -> run a prediction
"""

from typing import Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Personality Predictor API",
    description="Predicts Introvert vs Extrovert personality from behavioral traits.",
    version="1.0.0",
)

# Allow any frontend (Streamlit app, curl, Postman, etc.) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------------
# Load model + encoders once at startup
# ----------------------------------------------------------------------------
MODEL = joblib.load("personality_model.pkl")
ENCODERS = joblib.load("label_encoders.pkl")

FEATURE_ORDER = [
    "Time_spent_Alone",
    "Stage_fear",
    "Social_event_attendance",
    "Going_outside",
    "Drained_after_socializing",
    "Friends_circle_size",
    "Post_frequency",
]


# ----------------------------------------------------------------------------
# Request / response schemas
# ----------------------------------------------------------------------------
class PersonalityInput(BaseModel):
    Time_spent_Alone: float = Field(..., ge=0, description="Hours spent alone per day", json_schema_extra={"example": 4})
    Stage_fear: str = Field(..., description="'Yes' or 'No'", json_schema_extra={"example": "No"})
    Social_event_attendance: float = Field(..., ge=0, description="Events attended per month", json_schema_extra={"example": 5})
    Going_outside: float = Field(..., ge=0, description="Days per week going outside", json_schema_extra={"example": 4})
    Drained_after_socializing: str = Field(..., description="'Yes' or 'No'", json_schema_extra={"example": "No"})
    Friends_circle_size: float = Field(..., ge=0, description="Number of close friends", json_schema_extra={"example": 6})
    Post_frequency: float = Field(..., ge=0, description="Social media posts per week", json_schema_extra={"example": 4})


class PredictionOutput(BaseModel):
    prediction: str
    confidence: Optional[float] = None


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Personality Predictor API is running. See /docs for usage."}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionOutput)
def predict(payload: PersonalityInput):
    raw = payload.model_dump()

    row = {}
    for col in FEATURE_ORDER:
        val = raw[col]
        if col in ENCODERS:
            try:
                val = ENCODERS[col].transform([val])[0]
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid value '{val}' for '{col}'. "
                        f"Expected one of {list(ENCODERS[col].classes_)}."
                    ),
                )
        else:
            val = float(val)
        row[col] = val

    X_input = pd.DataFrame([row], columns=FEATURE_ORDER)
    pred = MODEL.predict(X_input)[0]

    if "Personality" in ENCODERS:
        label = ENCODERS["Personality"].inverse_transform([pred])[0]
    else:
        label = "Introvert" if pred == 1 else "Extrovert"

    # SVC was trained without probability=True, so there's no real
    # probability — use decision_function distance through a sigmoid
    # as a rough confidence-style signal instead.
    confidence = None
    try:
        score = MODEL.decision_function(X_input)[0]
        confidence = float(1 / (1 + np.exp(-abs(score))) * 100)
    except Exception:
        pass

    return PredictionOutput(prediction=str(label), confidence=confidence)
