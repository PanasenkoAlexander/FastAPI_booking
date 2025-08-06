from pydantic import BaseModel, ConfigDict
from typing import Dict, Any

class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: Dict[str, Any]  # JSON-объект хранится как словарь
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)  # Новый формат конфигурации


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)  # Новый формат конфигурации
