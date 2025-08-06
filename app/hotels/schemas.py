from pydantic import BaseModel, ConfigDict
from typing import Dict, Any

class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Dict[str, Any]  # JSON-объект хранится как словарь
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)  # Новый формат конфигурации


class SHotelInfo(SHotel):
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)  # Новый формат конфигурации
