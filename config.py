# Hello World program in Python
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    # JWT_REFRESH_TOKEN_EXPIRES = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_POOL_TIMEOUT=20
    SQLALCHEMY_DATABASE_URI = 'mysql://root:test1234@localhost/test'
    #UPLOAD_FOLDER = '/home/pravin/upload'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'alkakaushik.bsp@gmail.com'
    MAIL_PASSWORD = '98930a22418'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    
    
class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    # JWT_REFRESH_TOKEN_EXPIRES = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_POOL_TIMEOUT=20
    SQLALCHEMY_DATABASE_URI = 'mysql://root:test1234@localhost/test'
    #UPLOAD_FOLDER = '/home/pravin/upload'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'alkakaushik.bsp@gmail.com'
    MAIL_PASSWORD = '98930a22418'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI')