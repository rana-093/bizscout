from sqlalchemy.orm import Session
from sqlalchemy import func, case
from models import UsageEvent, ReportJob
from schemas import UsageEventCreate
from tasks import process_usage_data


def create_usage_event(db: Session, usage_event: UsageEventCreate) -> UsageEvent:
  db_event = UsageEvent(**usage_event.model_dump())
  db.add(db_event)
  db.commit()
  db.refresh(db_event)
  return db_event


def process_new_job(db: Session, user_id: int):
  db_event = ReportJob(
    user_id=user_id,
    status='IN_PROGRESS'
  )
  db.add(db_event)
  db.commit()
  db.refresh(db_event)
  process_usage_data.delay(user_id, db_event.id)
  return {'Job_id': db_event.id}


def get_job(db: Session, job_id: int):
  return (db.query(ReportJob)
          .filter(job_id).first())


def get_usage_events_by_user(db: Session, user_id: int):
  return (
    db.query(UsageEvent)
    .filter(UsageEvent.user_id == user_id)
    .all()
  )
  # return (
  #   db.query(
  #     UsageEvent.usage_type,
  #     func.sum(
  #       case(
  #         [(UsageEvent.usage_type.in_(["cpu_hours", "storage_gb"]), UsageEvent.usage_amount)],
  #         else_=0.0
  #       )
  #     ).label("total_usage"),
  #     func.avg(
  #       case(
  #         [(UsageEvent.usage_type == "memory", UsageEvent.usage_amount)],
  #         else_=None
  #       )
  #     ).label("avg_usage")
  #   )
  #   .filter(UsageEvent.user_id == user_id)
  #   .group_by(UsageEvent.usage_type)
  #   .all()
  # )
