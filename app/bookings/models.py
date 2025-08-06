from app.database import Base
from sqlalchemy import Column, Computed, Integer, Date, String, JSON, ForeignKey
from sqlalchemy.orm import relationship


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"))
    user_id = Column(ForeignKey("users.id"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
    total_days = Column(Integer, Computed("date_to - date_from"))

    # для связки в админке
    user = relationship("Users", back_populates="booking")
    room = relationship("Rooms", back_populates="booking")
    # для детального отображения данных в админке
    def __str__(self):
        return f"Booking #{self.id}"


# (1 раз только в начале) в терминале для создания миграций вводим: alembic init migrations
# (все время) затем прогон миграций: alembic revision --autogenerate -m "NAME of migration"
# (все время как вносим изменения в таблицы) затем для апгрейда таблицы: alembic upgrade head