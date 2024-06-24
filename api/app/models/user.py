from marshmallow import Schema, fields, validate, ValidationError
from app.utils.validation import validate_url_or_false
import re

PASSWORD_REGEX = {
    'uppercase': r'^(?=.*[A-Z])',
    'lowercase': r'^(?=.*[a-z])',
    'digit': r'^(?=.*\d)',
    'special': r'^(?=.*[@$!%*?&+#^(){}])',
    'length': r'^.{8,}$'
}

def validate_password(password):
    if not re.match(PASSWORD_REGEX['uppercase'], password):
        raise ValidationError("Password must contain at least one uppercase letter")
    if not re.match(PASSWORD_REGEX['lowercase'], password):
        raise ValidationError("Password must contain at least one lowercase letter")
    if not re.match(PASSWORD_REGEX['digit'], password):
        raise ValidationError("Password must contain at least one number")
    if not re.match(PASSWORD_REGEX['special'], password):
        raise ValidationError("Password must contain at least one special character @$!%*?&+#^(){}")
    if not re.match(PASSWORD_REGEX['length'], password):
        raise ValidationError("Password must be at least 8 characters long")

def validate_scholar_profile(url):
    if url is False:
        return True
    if not re.match(r'^https?://scholar\.google\.com/', url):
        raise ValidationError("Scholar profile URL must contain 'scholar.google.com/'")
    validate_url_or_false(url)

def validate_dblp_profile(url):
    if url is False:
        return True
    if not re.match(r'^https?://dblp\.org/', url):
        raise ValidationError("DBLP profile URL must contain 'https://dblp.org/'")
    validate_url_or_false(url)

def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        raise ValidationError("Username must contain only letters and numbers")

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
    username = fields.String(
        required=True,
        validate=[validate.Length(min=4, error="Username must be at least 4 characters long"), validate_username]
    )
    password = fields.String(
        required=True,
        validate=validate_password
    )
    name = fields.String(required=True, validate=validate.Length(min=1))
    scholar_profile = fields.Raw(required=True, validate=validate_scholar_profile)
    dblp_profile = fields.Raw(required=True, validate=validate_dblp_profile)
