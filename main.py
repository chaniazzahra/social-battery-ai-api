from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel

from inference import predict_social_battery_response


app = FastAPI(title="Social Battery AI API")


class CalendarEvent(BaseModel):
    title: str
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    durationMinutes: Optional[int] = 0
    isMovable: Optional[bool] = False


class SocialBatteryInput(BaseModel):
    batteryScore: float
    batteryStatus: str
    totalEvents: int
    totalDurationMinutes: float
    socialIntensityScore: float
    events: Optional[List[CalendarEvent]] = []


@app.get("/")
def home():
    return {
        "message": "Social Battery AI Service is running",
        "model": "mlp-recovery-strategy-v2"
    }


@app.post("/social-battery/insight")
def social_battery_insight(data: SocialBatteryInput):
    payload = data.dict()
    result = predict_social_battery_response(payload)
    return result