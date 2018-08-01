from app.models import Db
from app import create_app
import os
app = create_app(os.getenv("APP_SETTINGS"))
db_obj = Db(app)
db_obj.create_tables()