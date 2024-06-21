from marshmallow import Schema, fields, validate, ValidationError
from app.utils.validation import validate_url_or_false
class User:
    def __init__(self, _id, data, password):
        self._id = _id
        self.username = data["username"]
        self.password = password
        self.name = data["name"]
        self.scholar_profile = data["scholar_profile"]
        self.dblp_profile = data["dblp_profile"]

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password,
            'name': self.name,
            'dblp_profile': self.dblp_profile,
            'scholar_profile': self.scholar_profile
        }
    
class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))
    name = fields.String(required=True, validate=validate.Length(min=1))
    scholar_profile = fields.Raw(required=True, validate=validate_url_or_false)
    dblp_profile = fields.Raw(required=True, validate=validate_url_or_false)
