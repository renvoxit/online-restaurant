from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_login import login_required, current_user
from config import db
from models.models import Dish, Order, OrderItem

# Define the blueprint
main_bp = Blueprint('main', __name__)

# Define routes


@main_bp.route('/')
def index():
    return render_template('index.html')

# Menu route


@main_bp.route('/menu')
@login_required
def menu():
    dishes = Dish.query.all()
    return render_template('menu.html', dishes=dishes)

# Cart route


@main_bp.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

# Add to cart route


@main_bp.route('/add_to_cart/<int:dish_id>')
@login_required
def add_to_cart(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    cart = session.get('cart', [])
    cart.append({'id': dish.id, 'name': dish.name, 'price': dish.price})
    session['cart'] = cart
    return redirect(url_for('main.menu'))

# Checkout route


@main_bp.route('/checkout')
@login_required
def checkout():
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('main.menu'))
# Create order
    total = sum(item['price'] for item in cart)
    order = Order(user_id=current_user.id, total_price=total)
    db.session.add(order)
    db.session.flush()
# Add order items
    for item in cart:
        db.session.add(OrderItem(order_id=order.id,
                       dish_id=item['id'], quantity=1))
# Finalize
    db.session.commit()
    session['cart'] = []
# Confirmation
    flash('Order placed successfully!')
    return redirect(url_for('main.orders'))

# Order history route


@main_bp.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('order_history.html', orders=user_orders)
