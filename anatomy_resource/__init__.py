from flask import Flask, jsonify

from .config import config_map
from .extensions import db, migrate, jwt
from .main import main_bp
from .auth import auth_bp
from .auth.models import User
from .anatomy.models import AnatomyEntry
from .anatomy.routes import anatomy_bp


def create_app(config_name):
    app = Flask(__name__)

    config_class = config_map.get(config_name)

    if config_class is None:
        raise ValueError(f"Invalid configuration name: {config_name}")

    app.config.from_object(config_class)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise ValueError("DATABASE_URL must be set for this environment")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @jwt.invalid_token_loader
    def invalid_token_callback(error_message):
        return jsonify({"error": "Invalid or tampered token"}), 401

    

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(anatomy_bp)

    return app