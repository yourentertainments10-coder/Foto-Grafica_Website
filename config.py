import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///fotografica_dev.db")
    # Example of a production DATABASE_URL (do NOT commit credentials):
    # postgresql://user:password@host:port/dbname
SECRET_KEY = os.environ.get("SECRET_KEY", "dev_change_me")
class ProductionConfig(Config):
    DEBUG = False
