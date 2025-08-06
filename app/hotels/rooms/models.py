from app.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    # для связки в админке
    booking = relationship("Bookings", back_populates="room")
    hotel = relationship("Hotels", back_populates="rooms")

    # для детального отображения данных в админке
    def __str__(self):
        return f"Номер {self.name}"

# (1 раз только в начале) в терминале для создания миграций вводим: alembic init migrations
# (все время) затем прогон миграций: alembic revision --autogenerate -m "NAME of migration"
# (все время как вносим изменения в таблицы) затем для апгрейда таблицы: alembic upgrade head