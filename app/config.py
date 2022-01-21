from pydantic import BaseSettings


class Settings(BaseSettings):
    database_name: str
    secret_key: str
    jwt_algorithm: str
    token_expires_in: int

    class Config:
        env_file = '.env'


setting = Settings()