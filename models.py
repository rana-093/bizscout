from sqlalchemy import Column, Enum as SqlEnum, Integer, BigInteger, ForeignKey, Float, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from config.db import Base
import enum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UsageEvent(Base):
    __tablename__ = "usage_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    usage_type = Column(String, nullable=False)
    usage_unit = Column(String, nullable=True, default='percentage')
    usage_amount = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class ReportJob(Base):
    __tablename__ = "report_jobs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String, default="IN_PROGRESS")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    report_path = Column(String, nullable=True)


class AggregationType(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AggregatedSummary(Base):
    __tablename__ = "aggregated_summaries"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    computed_result = Column(Float, nullable=False)
    aggregation_type = Column(SqlEnum(AggregationType), nullable=False)
    aggregated_entity = Column(String, nullable=False)
