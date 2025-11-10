import os
from flask_sqlalchemy import SQLAlchemy


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db:5432/restaurant_db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
