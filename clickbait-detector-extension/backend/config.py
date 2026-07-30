from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

settings = Settings()