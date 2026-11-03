import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "replace-this-development-key")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "wifi.db")
    DEMO_MODE = os.getenv("DEMO_MODE", "1").lower() in ("1", "true", "yes")
    KISMET_URL = os.getenv("KISMET_URL", "http://127.0.0.1:2501").rstrip("/")
    KISMET_API_KEY = os.getenv("KISMET_API_KEY", "")
    KISMET_TIMEOUT = int(os.getenv("KISMET_TIMEOUT", "8"))
    FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
