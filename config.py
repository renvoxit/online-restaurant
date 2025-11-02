import os
from flask_sqlalchemy import SQLAlchemy


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///restaurant.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
