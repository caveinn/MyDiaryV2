'''create the app'''
import datetime
import jwt
from functools import wraps
from flask import Flask, request, jsonify
from instance.config import app_config
from app.models import user, entry
from werkzeug.security import generate_password_hash, check_password_hash

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
                print("decoded")
                usr = user(app.config.get('DB'))

                user_data = usr.get_all()

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
        user_ = user(app.config.get('DB'))
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
        entry_model = entry(app.config.get('DB'))
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
        user_obj = user(app.config.get('DB'))
        hashed_password = generate_password_hash(data["password"], method="sha256")
        user_obj.create(data["username"], hashed_password)
        return jsonify({"message":"user created"}), 201

    @app.route("/api/v2/entries", methods=['POST'])
    @token_required
    def create_entry(current_user):
        '''function to create  a new entry'''
        data = request.get_json()
        entry_model = entry(app.config.get('DB'))
        entry_model.create(data["title"], data["content"], current_user["id"])
        return jsonify({"message":"created succesfully"}), 201

    @app.route("/api/v2/entries/<entry_id>", methods=["PUT"])
    @token_required
    def modify_entry(current_user,entry_id):
        '''function to modify an entry'''
        entry_model = entry(app.config.get('DB'))
        data = request.get_json()
        entry_data = entry_model.get_all()
        exists = False
        for ent in entry_data:
            if int(ent["id"]) == int(entry_id):
                exists = True
                if int(ent["user_id"]) == int(current_user["id"]):
                    entry_model.update(id=entry_id,title=data["title"],content=data["content"])
                else:
                    return jsonify({"message":"you tried to acces a entry thats not yours"}), 401
        
        if not exists:
            return jsonify({"message":"entry does not exist"}), 401
        else:
            return jsonify({"message":"update succesful"})

    @app.route("/api/v2/entries/<ent_id>", methods=["DELETE"])
    @token_required
    def delete_entry(current_user,ent_id):
        '''function to delete an entry'''
        entry_model = entry(app.config.get('DB'))
        data = request.get_json()
        entry_data = entry_model.get_all()
        exists = False
        for ent in entry_data:
            if int(ent["id"]) == int(ent_id):
                exists = True
                if int(ent["user_id"]) == int(current_user["id"]):
                    entry_model.delete(entry_id=ent_id)
                else:
                    return jsonify({"message":"you tried to acces am entry thats not yours"}), 401
        
        if not exists:
            return jsonify({"message":"entry does not exist"}), 401
        else:
            return jsonify({"message":"entry deleted suuccessfully"})

    @app.route("/api/v2/entries/<entry_id>", methods = ["GET"])
    @token_required
    def get_single_entry(current_user, entry_id):
        '''function to modify an entry'''
        entry_model = entry(app.config.get('DB'))
        entry_data = entry_model.get_all()
        exists = False
        response = {"message":"could not get the entry"}
        for ent in entry_data:
            if int(ent["id"]) == int(entry_id):
                exists = True
                if int(ent["user_id"]) == int(current_user["id"]):
                    response = ent
                            
        if not exists:
            return jsonify(response), 400
        return jsonify(response)
                    
    return app
