from src.routes.test_routes import test_bp
from src.routes.user_routes import user_bp
def register_blueprints(app):
    app.register_blueprint(test_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/user")
    print(app.url_map)