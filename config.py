# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    PB_API_TOKEN = os.getenv("PB_API_TOKEN")
    PB_BASE_URL = os.getenv("PB_BASE_URL", "https://site-v2.apipb.ru")
    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.isdigit()]
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
    
    @classmethod
    def validate(cls):
        if not cls.TG_BOT_TOKEN or not cls.PB_API_TOKEN:
            raise ValueError("❌ Проверьте .env: TG_BOT_TOKEN и PB_API_TOKEN обязательны")

config = Config
config.validate()
