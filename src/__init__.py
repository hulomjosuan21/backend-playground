from flask import Flask
from src.register_blueprints import register_blueprints
from src.extensions import limiter, db, migrate, jwt, bcrypt
from flask_cors import CORS
from src.config import Config
from src.models import *

def initialize_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        db.create_all()

    register_blueprints(app)
    return app