"""FaskAPI configuration."""
from pydantic import BaseSettings
from functools import lru_cache
import os  
from dotenv import load_dotenv

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        
load_dotenv()
        
def getConfig():
    return Settings()

