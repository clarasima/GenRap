from flask import Blueprint
from .auth import bp as auth_bp
from .user import bp as user_bp
from .report import bp as report_bp
from .citations import bp as citations_bp
from .publications import bp as pub_bp
from .user_publications import bp as user_pub_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(citations_bp)
    app.register_blueprint(pub_bp)
    app.register_blueprint(user_pub_bp)
