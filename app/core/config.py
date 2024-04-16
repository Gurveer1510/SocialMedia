from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_connection_url : str
    access_token_expire : int 
    refresh_token_expire : int 
    secret_key : str
    algorithm : str
    api_v1_str: str


    class Config:
        env_file = ".env"

settings = Settings()