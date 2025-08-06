import smtplib
from app.config import settings
from app.tasks.celery_config import celery
from PIL import Image
from pathlib import Path
from pydantic import EmailStr
from app.tasks.email_templates import create_booking_confirmation_template
from app.logger import logger


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    for width, height in [
        (1000, 500),
        (200, 100)
    ]:
        resized_img = im.resize(size=(width, height))
        resized_img.save(f"app/static/images/resized_{width}_{height}_{im_path.name}")


@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    # для теста, если не хотим отправлять письмо на свою реальную почту, то используем иную email_to
    # и почта обязательно должна быть в базе
    # email_to = settings.SMTP_USER
    # указываем что отправить, с каким контентом
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
    logger.info(f"Successfully send email message to {email_to}")