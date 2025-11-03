from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from config import db
from models.models import Dish

admin_bp = Blueprint('admin', __name__)

# Admin panel route


@admin_bp.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.menu'))
    dishes = Dish.query.all()
    return render_template('admin.html', dishes=dishes)

# Add dish route


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

# Delete dish route


@admin_bp.route('/admin/delete/<int:dish_id>', methods=['POST'])
@login_required
def delete_dish(dish_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.menu'))

    dish = Dish.query.get_or_404(dish_id)
    db.session.delete(dish)
    db.session.commit()
    flash(f'Dish "{dish.name}" deleted successfully.')
    return redirect(url_for('admin.admin_panel'))

# Edit dish route


@admin_bp.route('/admin/edit/<int:dish_id>', methods=['GET', 'POST'])
@login_required
def edit_dish(dish_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.menu'))

    dish = Dish.query.get_or_404(dish_id)

    if request.method == 'POST':
        dish.name = request.form['name']
        dish.description = request.form['description']
        dish.price = float(request.form['price'])
        dish.image_url = request.form.get('image_url', '')
        db.session.commit()
        flash(f'Dish "{dish.name}" updated successfully.')
        return redirect(url_for('admin.admin_panel'))

    return render_template('edit_dish.html', dish=dish)

# View orders route


@admin_bp.route('/admin/orders')
@login_required
def view_orders():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.menu'))

    from models.models import Order
    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template('admin_orders.html', orders=orders)


@admin_bp.route('/admin/order/<int:order_id>/status', methods=['POST'])
@login_required
def change_order_status(order_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('main.menu'))

    from models.models import Order
    order = Order.query.get_or_404(order_id)
    new_status = request.form['status']
    order.status = new_status
    db.session.commit()
    flash(f'Order #{order.id} status updated to {new_status}.')
    return redirect(url_for('admin.view_orders'))
