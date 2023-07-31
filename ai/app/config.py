"""FaskAPI configuration."""
from pydantic import BaseSettings
from functools import lru_cache
import os  
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Settings(BaseSettings):
    ENV_STATE: str = 'dev'



@lru_cache
def getConfig() -> Settings:
    envfile = os.path.join(BASE_DIR, ".env")
    settings = Settings()
    print(os.environ["GENAI_KEY"])
    print(settings)
    return settings
