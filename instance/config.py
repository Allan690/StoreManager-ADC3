import os


class Config:
    # Parent config class
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")


class Development(Config):
    """development environment configurations"""
    DEBUG = True
    APP_SETTINGS = 'development'


class Testing(Config):
    """Testing environment configs"""
    DEBUG = True


class Production(Config):
    """Production environment configs"""
    DEBUG = False


# export the environment vars
app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}