from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    API_STR: str = '/api'
    PROJECT_NAME: str = 'recipe_server'
    SECRET_KEY: str = 'hackmeshepard'
    HOST: Union[str, None] = '0.0.0.0'
    PORT: Union[int, None] = 8080
    CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:3000'
    ]

    POSTGRES_USER: str = 'shepard'
    POSTGRES_PASSWORD = 'sheep123'
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: str = '5432'
    POSTGRES_DB: str = 'recipe_server'
    SQLALCHEMY_DATABASE_URL = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )

    class Config:
        case_sensitive = True


settings = Settings()
