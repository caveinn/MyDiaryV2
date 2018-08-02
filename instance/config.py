'''Set up environment specific configurations'''
import os

class Config():
    '''Parent configuration class'''
    DEBUG = False
    SECRET = os.getenv("SECRET")
    
class Development(Config):
    '''Configuration for development environment'''
    DEBUG = True
    DB = "dbname = test_db"

class Testing(Config):
    '''Configuration for testing environment'''
    WTF_CSRF_ENABLED = False
    DEBUG = True
    DB_NAME = "test_db"

class Production(Config):
    '''Configuration for production environment'''
    DEBUG = False
    DB = "dbname = diary"

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
