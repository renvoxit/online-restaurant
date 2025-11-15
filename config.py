import os
from flask_sqlalchemy import SQLAlchemy


import os
# Configuration class for Flask application


class Config:
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL") or "sqlite:///restaurant.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
