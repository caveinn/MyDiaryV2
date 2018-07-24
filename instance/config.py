'''Set up environment specific configurations'''

class Config():
    '''Parent configuration class'''
    DEBUG = False
    
class Development(Config):
    '''Configuration for development environment'''
    DEBUG = True

class Testing(Config):
    '''Configuration for testing environment'''
    WTF_CSRF_ENABLED = False
    DEBUG = True

class Production(Config):
    '''Configuration for production environment'''
    DEBUG = False

appConfig = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
