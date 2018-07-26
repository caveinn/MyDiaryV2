'''create the app'''
from flask import Flask
from instance.config import app_config
from app.models import db_table,user


def create_app(configName):
    app = Flask("__name__")
    app.config.from_object(app_config[configName])
    app.config.from_pyfile("instance/config.py")


    return app
