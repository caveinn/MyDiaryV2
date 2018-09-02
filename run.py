#app__init__.py
import os
from flask_cors import CORS
from app import create_app

NAME = os.getenv("APP_SETTINGS")
APP = create_app(configName=NAME)

if __name__ == "__main__":
    CORS(APP)
    APP.run()
