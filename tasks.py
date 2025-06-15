from config.celery_app import celery_app
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_, literal
from config.db import get_db, SessionLocal
from models import UsageEvent, ReportJob
import time
import asyncio
import datetime
from schemas import MetricData
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
from config.email import conf
from jinja2 import Environment, FileSystemLoader
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


def render_report_html(report_data: dict) -> str:
  env = Environment(loader=FileSystemLoader("templates"))
  template = env.get_template("reports.html")
  return template.render(report=report_data)


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

    non_percentage_metrics = db.query(
      UsageEvent.usage_type,
      UsageEvent.usage_unit,
      func.sum(UsageEvent.usage_amount).label("total_usage"),
      literal(None).label("avg_usage")
    ).filter(
      and_(
        UsageEvent.user_id == user_id,
        UsageEvent.usage_unit != "percentage"
      )
    ).group_by(UsageEvent.usage_type, UsageEvent.usage_unit)

    percentage_metrics = db.query(
      UsageEvent.usage_type,
      UsageEvent.usage_unit,
      literal(0.0).label("total_usage"),
      func.avg(UsageEvent.usage_amount).label("avg_usage")
    ).filter(
      and_(
        UsageEvent.user_id == user_id,
        UsageEvent.usage_unit == "percentage"
      )
    ).group_by(UsageEvent.usage_type, UsageEvent.usage_unit)

    metrics = non_percentage_metrics.union_all(percentage_metrics).all()

    if not result:
      return {"status": "no_data", "user_id": user_id}

    total_events = len(result)
    report_job.completed_at = datetime.datetime.now().isoformat()
    report_job.status = 'Completed'
    db.commit()
    report_data = {
      "user_id": user_id,
      "total_events": len(result),
      "metrics": [MetricData(
        usage_type=row.usage_type,
        usage_unit=row.usage_unit,
        total_usage=row.total_usage if row.total_usage != 0 else None,
        avg_usage=row.avg_usage
      ).dict() for row in metrics],
      "generated_at": datetime.datetime.now().isoformat(),
      "events": [
        {
          "usage_type": event.usage_type,
          "usage_amount": event.usage_amount,
          "created_at": event.timestamp.isoformat() if event.timestamp else None
        }
        for event in result
      ]
    }
    print(report_data)
    send_notification_email.delay(report_data, 'masudrana201505093@gmail.com')
    return report_data
  except Exception as e:
    print(f'Exception occured: {e}')
    report_job.status = 'Failed'
    db.commit()
  finally:
    db.close()


@celery_app.task
def send_notification_email(report_data: dict, to_user: str):
  try:
    html_content = render_report_html(report_data)

    message = MessageSchema(
      subject="Your Usage Report",
      recipients=[to_user],
      body=html_content,
      subtype="html"
    )

    fm = FastMail(conf)
    asyncio.run(fm.send_message(message))
  except Exception as e:
    print(e)
