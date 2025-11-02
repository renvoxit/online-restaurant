from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from config import db
from models.models import Dish

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.menu'))
    dishes = Dish.query.all()
    return render_template('admin.html', dishes=dishes)


@admin_bp.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_dish():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.menu'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_url = request.form.get('image_url', '')
        db.session.add(Dish(name=name, description=description,
                       price=price, image_url=image_url))
        db.session.commit()
        flash('Dish added')
        return redirect(url_for('admin.admin_panel'))
    return render_template('add_dish.html')
