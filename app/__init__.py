'''create the app'''
import datetime
import jwt
from functools import wraps
from flask import Flask, request, jsonify
from instance.config import app_config
from app.models import db_table, user, entry
from werkzeug.security import generate_password_hash, check_password_hash



def create_app(configName):
    app = Flask("__name__")
    app.config.from_object(app_config[configName])
    app.config.from_pyfile("instance/config.py")

    @app.route("/api/v2/auth/login", methods=["POST"])
    def login():
        '''function ot log in user'''
        user_ = user()
        user_data = user_.get_all()
        auth = request.authorization
        resp = None
        token = None
        for single_user in user_data:
            if auth["username"] == single_user["username"] and \
            check_password_hash(single_user["password"],auth["password"]):
                token = jwt.encode(
                    {"username":single_user["username"], 'exp': datetime.datetime.utcnow()+
                    datetime.timedelta(minutes=300)}, "some long text which is secret")
                resp = jsonify({"token":token.decode("UTF-8")})
        if token is None:
            resp = jsonify({"message":"could not log in"})
            resp.status_code=401
        return resp

    
    return app
