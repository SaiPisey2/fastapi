from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_pass: str = "localhost"
    db_user: str = "postgres"
    db_host: str 
    db_name: str
    db_port: str
    algorithm : str
    secret_key: str 
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()