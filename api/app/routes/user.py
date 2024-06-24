from flask import Blueprint, request, jsonify, abort
from app import users_collection
from app.models.user import User, UserSchema
from app.utils.validation import format_errors
from app.utils.auth import token_required
import uuid
from werkzeug.security import generate_password_hash
from marshmallow import ValidationError

bp = Blueprint('user', __name__)

user_schema = UserSchema()

# Sign Up
@bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user_schema.load(data)
    except ValidationError as err:
        error_message = format_errors(err.messages)
        return jsonify({"errors": error_message}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(_id=data["username"], data=data, password=hashed_password)
    try:
        result = users_collection.insert_one(new_user.to_dict())
        if result.acknowledged:
            return jsonify({'result': 'User added', 'user_id': str(result.inserted_id)}), 201 # 201 Created
        else:
            abort(500, description="An error occurred: Failed to add user")
    except Exception as e:
        if "duplicate key error" in str(e):
            abort(409, description="Username already exists")
        else:
            abort(500, description=f"An error occurred: {e}")

# data about the user from My profile
@bp.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user_by_id(user_id):
    try:
        user = users_collection.find_one({"_id": user_id})

        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user)
        else:
            abort(404, description="User not found")
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")

# currently unused
@bp.route('/user/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    try:
        result = users_collection.delete_one({"_id": user_id})

        if result.deleted_count > 0:
            return jsonify({"result": "User deleted"})
        else:
            abort(404, description="User not found")
    except Exception as e:
        abort(500, description=f"An error occurred: {e}")
