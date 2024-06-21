from functools import wraps
from flask import request, jsonify, abort
import jwt
from app import users_collection
from app.config import config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
            user = users_collection.find_one({"_id": data["_id"]})

            if not user:
                return jsonify({'message': 'User not found'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            abort(500, description=f"An error occurred: {e}")

        return f(*args, **kwargs)

    return decorated
