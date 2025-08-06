from email.message import EmailMessage
from app.config import settings
from pydantic import EmailStr


def create_booking_confirmation_template(
    booking: dict,
    hotels: dict,
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    # содержание письма
    email.set_content(
        f""""
            <h1>Подтвердите бронирование</h1>
            Вы забронировали {hotels["name"]} с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html"
    )
    return email
