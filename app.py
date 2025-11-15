from flask import Flask
from config import Config
from models.models import User
from extensions import db, login_manager, csrf, migrate, limiter
from models.models import Dish
from seed_menu import seed_menu

if Dish.query.count() == 0:
    seed_menu()


login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_pyfile('config.py', silent=True)

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

    from models.models import User
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            is_admin=True
        )
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()

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
