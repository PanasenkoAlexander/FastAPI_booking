from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: int
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: int
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()

# для получения ключа необходимо вызвать python, затем вставить 4 строки ниже
# from secrets import token_bytes
# from base64 import b64encode
#
# print(b64encode(token_bytes(32)).decode())