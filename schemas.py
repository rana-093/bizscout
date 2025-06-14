from pydantic import BaseModel


class UsageEventCreate(BaseModel):
    user_id: int
    usage_type: str
    usage_amount: float
