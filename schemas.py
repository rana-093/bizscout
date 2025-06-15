from pydantic import BaseModel
from typing import List, Optional

class UsageEventCreate(BaseModel):
    user_id: int
    usage_type: str
    usage_amount: float
    usage_unit: str


class MetricData(BaseModel):
    usage_type: str
    usage_unit: str
    total_usage: Optional[float]
    avg_usage: Optional[float]
