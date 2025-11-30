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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root%40123@localhost/foto-grafica'
    #SQLALCHEMY_DATABASE_URL="postgresql://fotografica_user:iGbw7h5dEDq6kEP612pYS88x4zTw6Ufi@dpg-d3dl8lbe5dus73bou7p0-a/fotografica"
    SECRET_KEY="mysecretkey"
class ProductionConfig(Config):
    DEBUG = False
