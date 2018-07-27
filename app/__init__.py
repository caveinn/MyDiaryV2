'''create the app'''
import datetime
import jwt
from functools import wraps
from flask import Flask, request, jsonify
from instance.config import app_config
from app.models import db_table, user, entry
from werkzeug.security import generate_password_hash, check_password_hash

#wrapper to to confirm authentication
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwags):
        token = None
        current_user = None
        if "access_token" in request.headers:
            token = request.headers["access_token"]
        if not token:
            return jsonify({"message":"no token specified"}), 401
        try:
            data = jwt.decode(token, "some long text which is secret")
            usr = user()

            user_data = usr.get_all()

            for single_user in user_data:
                if single_user["username"] == data["username"]:
                    current_user = single_user

        except Exception as e:

            return jsonify({"message":"invalid token"}), 401
        return func(current_user, *args, **kwags)
    return decorated

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
            if single_user and auth:
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

    @app.route("/api/v2/entries", methods=["GET"])
    @token_required
    def get_entries(current_user):
        '''function get all entries for the user'''
        entry_model = entry()
        data = {}
        data = entry_model.get_all()
        data_to_show=[]
        for ent in data:
            if ent['user_id'] == current_user["id"]:
                data_to_show.append(ent)
        return jsonify(data_to_show)

    @app.route("/api/v2/auth/signup", methods=['POST'])
    def create_user():
        '''function to signup user'''
        data = request.get_json()
        user_obj = user()
        hashed_password = generate_password_hash(data["password"], method="sha256")
        user_obj.create(data["username"], hashed_password)
        return jsonify({"message":"user created"}), 201

   
                    
    return app
