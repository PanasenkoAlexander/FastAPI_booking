from app.database import Base
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    # для связки в админке
    rooms = relationship("Rooms", back_populates="hotel")
    # для детального отображения данных в админке
    def __str__(self):
        return f"Отель {self.name} {self.location[:30]}"

# (1 раз только в начале) в терминале для создания миграций вводим: alembic init migrations
# (все время) затем прогон миграций: alembic revision --autogenerate -m "NAME of migration"
# (все время как вносим изменения в таблицы) затем для апгрейда таблицы: alembic upgrade head