from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import check_password_hash
from datetime import datetime, timezone
import datetime as dt
import jwt
from app import users_collection
from app.config import config

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        print("Bad Request: Username and password required.")
        return make_response('Bad Request: Username and password required.', 400, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = users_collection.find_one({"username": auth.username})
    if not user:
        print("'Username does not exist in the database.'")
        return make_response('Username does not exist in the database.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user["password"], auth.password):
        expiration = datetime.now(tz=timezone.utc) + dt.timedelta(hours=24)
        token = jwt.encode({'_id': user["_id"], 'exp': expiration}, config.SECRET_KEY)
        return jsonify({'token': token})
    print("not verify")
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
