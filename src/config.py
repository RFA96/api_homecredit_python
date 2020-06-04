from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(verbose=True)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Development(object):
    """
        Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class Production(object):
    """
        Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


app_config = {
    'development': Development,
    'production': Production,
}
