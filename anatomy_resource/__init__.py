from flask import Flask
from .config import config_map
from .extensions import db, migrate
from .main import main_bp

def create_app(config_name):
    app = Flask(__name__)

    config_class = config_map.get(config_name)

    if config_class is None:
        raise ValueError(f"Invalid configuration name: {config_name}")

    app.config.from_object(config_class)


    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)

    return app