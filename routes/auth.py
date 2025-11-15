from flask_login import login_user, logout_user, login_required, current_user
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.models import User
from extensions import db, limiter

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('User with this username or email already exists')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5/minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin.admin_panel'))
            return redirect(url_for('main.menu'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Route to create admin user and seed menu


@auth_bp.route("/create_admin_now", methods=["GET"])
def create_admin_now():
    from models.models import User, Dish
    from seed_menu import seed_menu

    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@example.com",
            is_admin=True,

        )
        admin.set_password("admin")
        db.session.add(admin)

    if Dish.query.count() == 0:
        seed_menu()

    db.session.commit()
    return "ADMIN + MENU CREATED"
