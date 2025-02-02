import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)


class EmailServiceConfig(BaseSettings):
    smtp_server: str
    smtp_port: int
    username: str
    password: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix='email_')


class EmailService:
    def __init__(self, config: EmailServiceConfig):
        self.smtp_server = config.smtp_server
        self.smtp_port = config.smtp_port
        self.username = config.username
        self.password = config.password

    def send_email(self, to_email: str, subject: str, body: str):
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, to_email, msg.as_string())
                logger.info(f"Email sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
