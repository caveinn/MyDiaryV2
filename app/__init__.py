'''create the app'''
import datetime
from functools import wraps
import jwt
from flask import Flask, request, jsonify
from instance.config import app_config
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Entry, Db

#wrapper to to confirm authentication


def create_app(configName):
    app = Flask("__name__")
    app.config.from_object(app_config[configName])
    app.config.from_pyfile("instance/config.py")

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
                data = jwt.decode(token, app.config.get("SECRET"))
                db_object = Db()

                user_data = db_object.get_all_users()
                for single_user in user_data:

                    if single_user["username"]== data["username"]:
                        current_user = single_user

            except Exception as e:
                print(e)
                return jsonify({"message":"invalid token"}), 401
            return func(current_user, *args, **kwags)
        return decorated

    @app.route("/api/v2/auth/login", methods=["POST"])
    def login():
        '''function ot log in user'''
        db_object = Db()
        user_data = db_object.get_all_users()
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        resp = None
        token = None
        for single_user in user_data:
            if single_user and  username and password:
                if username == single_user["username"] and \
                check_password_hash(single_user["password"],password):
                    token = jwt.encode(
                        {"username":single_user["username"], 'exp': datetime.datetime.utcnow()+
                        datetime.timedelta(minutes=300)}, app.config.get("SECRET"))
                    resp = jsonify({"token":token.decode("UTF-8")})
        if token is None:
            resp = jsonify({"message":"could not log in"})
            resp.status_code=401
        return resp

    @app.route("/api/v2/entries", methods=["GET"])
    @token_required
    def get_entries(current_user):
        '''function get all entries for the user'''
        db = Db()
        entries = db.get_all_entries()
        print(entries)
        data_to_show = []
        for ent in entries:

            if ent['user_id'] == current_user["id"]:
                data_to_show.append(ent)
        return jsonify(data_to_show)

    @app.route("/api/v2/auth/signup", methods=['POST'])
    def create_user():
        '''function to signup user'''
        data = request.get_json()
        hashed_password = generate_password_hash(data["password"], method="sha256")
        user_obj = User(data["username"], data["email"], hashed_password)

        return jsonify({"message":"user created"}, user_obj.get_data()), 201

    @app.route("/api/v2/entries", methods=['POST'])
    @token_required
    def create_entry(current_user):
        '''function to create  a new entry'''
        data = request.get_json()
        entry_obj = Entry(title=data["title"], content = data["content"], user_id =current_user["id"] )
        return jsonify({"message":"created succesfully"}), 201

    @app.route("/api/v2/entries/<entry_id>", methods=["PUT"])
    @token_required
    def modify_entry(current_user,entry_id):
        '''function to modify an entry'''
        db = Db()
        data = request.get_json()
        entry_data = db.get_all_entries()
        exists = False
        for ent in entry_data:
            if int(ent["id"]) == int(entry_id):
                exists = True
                if int(ent["user_id"]) == int(current_user["id"]):
                    db.update(entry_id=entry_id,title=data["title"],content=data["content"])
                else:
                    return jsonify({"message":"you tried to acces a entry thats not yours"}), 401
        
        if not exists:
            return jsonify({"message":"entry does not exist"}), 401
        else:
            return jsonify({"message":"update succesful"})


    @app.route("/api/v2/entries/<entry_id>", methods = ["GET"])
    @token_required
    def get_single_entry(current_user, entry_id):
        '''function to modify an entry'''
        db = Db()
        entries = db.get_all_entries()
        entry = {"message":"could not find your entry"}
        print(entries)
        print(current_user)
        for ent in entries:
            if int(ent['user_id']) == int(current_user["id"]) and int(ent["id"]) == int(entry_id):
                entry=ent  
        return jsonify(entry)
                    
    return app
