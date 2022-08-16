from pydantic import BaseSettings


class Settings(BaseSettings):
    happy_playlist_id:str
    sad_playlist_id:str
    neutral_playlist_id:str
    client_secret:str
    client_id:str

    class Config:
        env_file = '.env'

settings = Settings()