from flask import Flask
from config import Config
from models.models import User
from extensions import db, login_manager, csrf, migrate, limiter

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_pyfile('config.py', silent=True)

# Initialize extensions

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    @app.after_request
    def set_headers(resp):
        resp.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
        )
        return resp

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
