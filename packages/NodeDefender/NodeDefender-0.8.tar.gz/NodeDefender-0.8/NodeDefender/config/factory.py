import NodeDefender

class DefaultConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = None
    SECRET_SALT = None
    SERVER_NAME = '127.0.0.1:5000'
    PORT = 5000
    SELF_REGISTRATION = True
    WTF_CSRF_ENABLED = False
    
    DATABASE = False
    REDIS = False
    LOGGING = False
    MAIL = False
    CELERY = False

class TestingConfig(DefaultConfig):
    TESTING = True
    DATABASE = False
    LOGGING = False
    MAIL = False
    CELERY = False
