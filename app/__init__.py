'''create the app'''
import datetime
import jwt
from flask import Flask, request, jsonify
from instance.config import app_config
from app.models import db_table, user, entry


def create_app(configName):
    app = Flask("__name__")
    app.config.from_object(app_config[configName])
    app.config.from_pyfile("instance/config.py")

    @app.route("/api/v2/auth/login", methods=["POST"])
    def login():
        user_ = user()
        user_dict = user_.get_all()
        auth = request.authorization
        resp = None
        token = None
        for single_user in user_dict.values():
            if auth["username"] == single_user["username"] and \
            auth["password"] == single_user["password"]:
                token = jwt.encode(
                    {"username":single_user["username"], 'exp': datetime.datetime.utcnow()+
                    datetime.timedelta(minutes=30)}, "some long text which is secret")
                resp = jsonify({"token":token.decode("UTF-8")})
        if token is None:
            resp = jsonify({"message":"could not log in"})
            resp.status_code=401
        return resp

    return app
