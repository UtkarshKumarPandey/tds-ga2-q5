from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_1wg743n9he4v2h5yenna6oy3"
EMAIL = "23f3003796@ds.study.iitm.ac.in"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/analytics")
def analytics(
    body: AnalyticsRequest,
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    revenue = 0.0
    user_totals = {}

    for event in body.events:
        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] = user_totals.get(event.user, 0.0) + event.amount

    top_user = ""
    if user_totals:
        top_user = max(user_totals.items(), key=lambda x: x[1])[0]

    return {
        "email": EMAIL,
        "total_events": len(body.events),
        "unique_users": len({event.user for event in body.events}),
        "revenue": revenue,
        "top_user": top_user,
    }
