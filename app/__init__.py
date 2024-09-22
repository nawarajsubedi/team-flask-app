from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate
from app.routes import main_bp


def create_app(config_class=Config):
    """
    Flask Application Factory to create and configure the app instance.
    """
    app = Flask(__name__)

    app.config.from_object(config_class)
    
    # Configure CORS
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    register_blueprints(app)

    return app

def register_blueprints(app: Flask):
    """
    Register all blueprints with the Flask application instance.
    """
    app.register_blueprint(main_bp, url_prefix="/api/v1")
