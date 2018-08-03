'''create the app'''
import datetime
from functools import wraps
import re
import jwt
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Entry, Db
from instance.config import app_config

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

                    if single_user["username"] == data["username"]:
                        current_user = single_user

            except Exception as e:
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
        data_to_show = []
        for ent in entries:

            if ent['user_id'] == current_user["id"]:
                data_to_show.append(ent)
        return jsonify(data_to_show)

    @app.route("/api/v2/auth/signup", methods=['POST'])
    def create_user():
        '''function to signup user'''
        data = request.get_json()
        db_obj = Db()
        username = data["username"].strip()
        email = data["email"].strip()
        user_data = db_obj.get_all_users()
        for single_user in user_data:
            if single_user["username"] == username:
                return jsonify({"message":"user "+ data['username']+" is already registered"}), 400
            if single_user["email"] == email:
                return jsonify({"message":"email "+ email +" is already registered"}), 400
        if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email):
            return jsonify({'message':'invalid email'}), 400
        if username == '':
            return jsonify({"message":"username cannot be blank"}), 400
        if data["password"] == '':
            return jsonify({"message":"password cannot be blank"}), 400
        hashed_password = generate_password_hash(data["password"], method="sha256")
        user_obj = User(data["username"], data["email"], hashed_password)

        return jsonify(user_obj.get_data()), 201

    @app.route("/api/v2/entries", methods=['POST'])
    @token_required
    def create_entry(current_user):
        '''function to create  a new entry'''
        data = request.get_json()
        db_obj = Db()
        entry_data = db_obj.get_all_entries()
        for single_entry in entry_data:
            if single_entry["title"] == data["title"] and single_entry["user_id"] == current_user["id"]:
                return jsonify({"message":"entry with title "+ data['title']+" already exists"}), 400
        if data["title"].strip() == '':
            return jsonify({"message":"title cannot be blank"}), 400
        if data["content"].strip() == '':
            return jsonify({"message":"content cannot be blank"}), 400

        entry_obj = Entry(title=data["title"], content = data["content"], user_id =current_user["id"] )
        return jsonify(entry_obj.get_data()), 201

    @app.route("/api/v2/entries/<entry_id>", methods=["PUT"])
    @token_required
    def modify_entry(current_user,entry_id):
        '''function to modify an entry'''
        data = request.get_json()
        db_obj = Db()
        entry = db_obj.update(entry_id, data["title"], data["content"], current_user["id"])
        return entry
        
    @app.route("/api/v2/entries/<entry_id>", methods=["DELETE"])
    @token_required
    def delete_entry(current_user,entry_id):
        '''function to modify an entry'''
        db = Db()
        entry_data = db.get_all_entries()
        entry_to_del = None
        for ent in entry_data:
            if int(ent["id"]) == int(entry_id):
                if int(ent["user_id"]) == int(current_user["id"]):
                    entry_to_del = ent
                    db.delete(entry_id=entry_id)
                    return jsonify(entry_to_del)
                return jsonify({"message":"you tried to access a entry thats not yours"}), 400
        return jsonify({"message":"entry does not exist"}), 400

    @app.route("/api/v2/entries/<entry_id>", methods=["GET"])
    @token_required
    def get_single_entry(current_user, entry_id):
        '''function to modify an entry'''
        db = Db()
        entries = db.get_all_entries()
        entry = {"message":"could not find your entry"}
        for ent in entries:
            if int(ent['user_id']) == int(current_user["id"]) and int(ent["id"]) == int(entry_id):
                entry=ent  
        return jsonify(entry)
                    
    return app
