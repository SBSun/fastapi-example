import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Task

from config import get_settings

settings = get_settings()

# celery에서 제공하는 Task 클래스를 상속받는다.
class SendWelcomeEmailTask(Task):
    name = "send_welcome_email_task"

    def run(self, receiver_email: str):
        sender_email = "byung0216@gmail.com"
        password = settings.email_password

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "회원 가입을 환영합니다."

        body = "TIL 서비스를 이용해주셔서 감사합니다."
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(message)