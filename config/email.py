import os
from config.settings import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
  MAIL_USERNAME=settings.email_host_user,
  MAIL_PASSWORD=settings.email_host_password,
  MAIL_FROM=settings.email_host_user,
  MAIL_PORT=settings.email_port,
  MAIL_SERVER=settings.email_host,
  MAIL_STARTTLS=True,
  MAIL_SSL_TLS=False,
  USE_CREDENTIALS=True,
  TEMPLATE_FOLDER="templates"
)
