import os
from functools import lru_cache

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from noshow.model import NoShowModel

app = FastAPI(title="No-show predictor")


class Flight(BaseModel):
    route: str
    hour: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)
    month: int = Field(ge=1, le=12)
    booked_passengers: int = Field(gt=0)
    advance_booking_days: float = Field(ge=0)
    flex_share: float = Field(ge=0, le=1)
    connecting_share: float = Field(ge=0, le=1)


@lru_cache
def get_model() -> NoShowModel:
    return NoShowModel.load(os.getenv("MODEL_PATH", "artifacts/model.joblib"))


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict")
def predict(flight: Flight) -> dict:
    try:
        model = get_model()
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Model not available")
    rate = float(model.predict(pd.DataFrame([flight.model_dump()]))[0])
    return {
        "no_show_rate": round(rate, 4),
        "expected_no_shows": round(rate * flight.booked_passengers, 1),
    }
