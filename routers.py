from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from config.db import get_db

usage_router = APIRouter(prefix="/usage", tags=["usage"])
report_router = APIRouter(prefix="/reports", tags=["reports"])


@usage_router.post("/")
def submit_usage_event(usage_event: schemas.UsageEventCreate, db: Session = Depends(get_db)):
    return crud.create_usage_event(db, usage_event)


@usage_router.get("/{user_id}")
def get_usage_events(user_id: int, db: Session = Depends(get_db)):
    events = crud.get_usage_events_by_user(db, user_id)
    if not events:
        raise HTTPException(status_code=404, detail="User not found or no events")
    return events


@report_router.post("/{user_id}")
def process_report(user_id: int, db: Session = Depends(get_db)):
    return crud.process_new_job(db, user_id)


@report_router.post("/status/{job_id}")
def process_report(user_id: int, db: Session = Depends(get_db)):
    return crud.get_job(db, user_id)
