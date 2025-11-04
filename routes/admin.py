from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import Dish, Order
from app import db, limiter

admin_bp = Blueprint('admin', __name__)

# Admin Panel Route


@admin_bp.route('/admin', methods=['GET'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.menu'))
    dishes = Dish.query.all()
    return render_template('admin.html', dishes=dishes)

# Add Dish Route


@admin_bp.route('/admin/add', methods=['POST'])
@login_required
def add_dish():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.menu'))

    name = request.form['name']
    try:
        price = float(request.form['price'])
    except ValueError:
        flash('Invalid price format.')
        return redirect(url_for('admin.admin_panel'))

    new_dish = Dish(name=name, price=price)
    db.session.add(new_dish)
    db.session.commit()
    flash('Dish added successfully.')
    return redirect(url_for('admin.admin_panel'))

# Edit Dish Route


@admin_bp.route('/admin/edit/<int:dish_id>', methods=['GET', 'POST'])
@login_required
def edit_dish(dish_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.menu'))

    dish = Dish.query.get_or_404(dish_id)

    if request.method == 'POST':
        dish.name = request.form['name']
        dish.description = request.form.get('description', '')
        try:
            dish.price = float(request.form['price'])
        except ValueError:
            flash('Invalid price format.')
            return redirect(url_for('admin.edit_dish', dish_id=dish.id))
        dish.image_url = request.form.get('image_url', '')
        db.session.commit()
        flash('Dish updated successfully.')
        return redirect(url_for('admin.admin_panel'))

    return render_template('edit_dish.html', dish=dish)

# Delete Dish Route


@admin_bp.route('/admin/delete/<int:dish_id>', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def delete_dish(dish_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.menu'))

    dish = Dish.query.get_or_404(dish_id)
    db.session.delete(dish)
    db.session.commit()
    flash('Dish deleted successfully.')
    return redirect(url_for('admin.admin_panel'))

# View Orders Route


@admin_bp.route('/admin/orders')
@login_required
def view_orders():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.menu'))

    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template('admin_orders.html', orders=orders)

# Change Order Status Route


@admin_bp.route('/admin/change_status/<int:order_id>', methods=['POST'])
@login_required
def change_order_status(order_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.menu'))

    order = Order.query.get_or_404(order_id)
    new_status = request.form['status']
    order.status = new_status
    db.session.commit()
    flash(f'Order #{order.id} status updated to {new_status}.')
    return redirect(url_for('admin.view_orders'))
