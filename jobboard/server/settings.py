import os
from typing import Optional

from pydantic import EmailStr, HttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Jobboard"
    API_VI_STR: str = "/api/jobboard/v1"
    ELASTIC_PORT: int
    ELASTIC_HOST: str
    ELASTIC_PASSWORD: Optional[str] = None
    ELASTIC_USERNAME: str
    CACHE_PORT: int
    CACHE_HOST: str
    CACHE_DB: int = 0
    CACHE_SSL: Optional[bool] =  False
    ELASTIC_SSL: Optional[bool] = False
    PAGINATION_PAGE_SIZE: int = 20
    JOB_API_KEY: str
    ADMIN_EMAIL: EmailStr

    @field_validator("ELASTIC_SSL", mode="before")
    @classmethod
    def validate_elastic_ssl(cls, field: bool):
        if field is True and not os.environ.get("ELASTIC_CERT_PATH"):
            raise ValueError("Elastic search certificate path is required in SSL mode")

    @field_validator("CACHE_SSL", mode="before")
    @classmethod
    def validate_cache_ssl(cls, field: bool):
        if field is True and not os.environ.get("CACHE_CERT_PATH"):
            raise ValueError("Redis certificate path is required in SSL mode")


settings = Settings()
