import os
from app import createApp

name=os.getenv("APP_SETTINGS")
app=createApp(configName=name)

if __name__=="__main__":
	app.run()