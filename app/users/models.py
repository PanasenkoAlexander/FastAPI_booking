from app.database import Base
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # для связки в админке
    booking = relationship("Bookings", back_populates="user")
    # для детального отображения юзера в админке
    def __str__(self):
        return f"Пользователь {self.email}"


# далее в терминале для создания миграций вводим: alembic init migrations
# затем прогон миграций: alembic revision --autogenerate -m "Initial migration"
# затем для апгрейда таблицы: alembic upgrade head