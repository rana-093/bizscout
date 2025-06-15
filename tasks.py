from config.celery_app import celery_app
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from config.db import get_db, SessionLocal
from models import UsageEvent, ReportJob
import time
import datetime


@celery_app.task
def process_usage_data(user_id: int, job_id: int):
    db: Session = SessionLocal()
    report_job = db.query(ReportJob).get(job_id)
    if not report_job:
        return
    try:
        result = (
          db.query(UsageEvent)
          .filter(UsageEvent.user_id == user_id)
          .all()
        )

        metrics = db.query(
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
        ).filter(UsageEvent.user_id == user_id).group_by(UsageEvent.usage_type).all()

        if not result:
          return {"status": "no_data", "user_id": user_id}

        total_events = len(result)
        report_job.status = 'Completed'
        db.commit()
        report_data = {
          "user_id": user_id,
          "total_events": len(result),
          "metrics": [dict(row._mapping) for row in metrics],
          "generated_at": datetime.datetime().isoformat(),
          "events": [
            {
              "usage_type": event.usage_type,
              "usage_amount": event.usage_amount,
              "created_at": event.created_at.isoformat() if event.created_at else None
            }
            for event in result
          ]
        }
        return report_data
    except:
        report_job.status = 'Failed'
        db.commit()
    finally:
        db.close()


@celery_app.task
def send_notification_email(user_id: int, message: str):
    pass
