from pydantic_settings import BaseSettings
from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  PROJECT_NAME: str = "BizScout"
  VERSION: str = "1.0.0"
  API_V1_STR: str = "/api/v1"

  # Database
  DATABASE_URL: str
  DATABASE_URL_SYNC: str

  # Security
  SECRET_KEY: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

  # Environment
  DEBUG: bool = False

  email_host: str
  email_host_user: str
  email_host_password: str
  email_port: int

  class Config:
    env_file = ".env"


settings = Settings()
