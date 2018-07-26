#app__init__.py
import os
from app import create_app

name = os.getenv("APP_SETTINGS")
app = create_app(configName=name)

if __name__ == "__main__":
    app.run()
