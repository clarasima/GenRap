from marshmallow import Schema, fields

class Report:
    def __init__(self, _id, user_id, content):
        self._id = _id
        self.user_id = user_id
        self.content = content

    def to_dict(self):
        return {
            '_id': self._id,
            'user_id': self.user_id,
            'content': self.content
        }

class ReportSchema(Schema):
    user_id = fields.String(required=True)
    content = fields.String(required=True)
