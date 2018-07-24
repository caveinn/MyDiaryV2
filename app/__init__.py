from flask import Flask
from instance.config import appConfig

def createApp(configName):
	app=Flask("__name__")
	app.config.from_object(appConfig[configName])
	app.config.from_pyfile("instance/config.py")


	return app
