from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from app.config import config

app = Flask(__name__)
CORS(app)

# Initialize MongoDB client
client = MongoClient(config.DB_URI)
db = client['report_generator']
users_collection = db['users']
publications_collection = db['publications']
citations_collection = db['citations']

from app.routes import register_blueprints
register_blueprints(app)
