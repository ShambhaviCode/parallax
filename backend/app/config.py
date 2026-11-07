import os

APP_NAME = "PARALLAX Incident Intelligence API"
VERSION = "1.0.0"
DATABASE_URL = os.getenv("PARALLAX_DATABASE_URL", "sqlite:///./parallax.db")
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("PARALLAX_CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]
