from sqlalchemy.orm import Session
from sqlalchemy import func, case
from models import UsageEvent
from schemas import UsageEventCreate


def create_usage_event(db: Session, usage_event: UsageEventCreate) -> UsageEvent:
    db_event = UsageEvent(**usage_event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_usage_events_by_user(db: Session, user_id: int):
  return (
    db.query(
      UsageEvent.usage_type,
      func.sum(
        case(
          [(UsageEvent.usage_type.in_(["cpu_hours", "storage_gb"]), UsageEvent.usage_amount)],
          else_=0.0
        )
      ).label("total_usage"),
      func.avg(
        case(
          [(UsageEvent.usage_type == "memory", UsageEvent.usage_amount)],
          else_=None
        )
      ).label("avg_usage")
    )
    .filter(UsageEvent.user_id == user_id)
    .group_by(UsageEvent.usage_type)
    .all()
  )
