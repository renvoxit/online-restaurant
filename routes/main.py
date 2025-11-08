from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_login import login_required, current_user
from extensions import db, limiter
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

# Check if dish already in cart

    for item in cart:
        if item['id'] == dish.id:
            item['quantity'] += 1
            break
    else:
        cart.append({
            'id': dish.id,
            'name': dish.name,
            'price': dish.price,
            'quantity': 1,
            'image_url': dish.image_url if hasattr(dish, 'image_url') else None
        })

    session['cart'] = cart

    referrer = request.referrer or ""
    if "cart" in referrer:
        return redirect(url_for('main.cart'))
    else:
        return redirect(url_for('main.menu'))

# Remove from cart route


@main_bp.route('/remove_from_cart/<int:dish_id>')
@login_required
def remove_from_cart(dish_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != dish_id]
    session['cart'] = cart
    flash('Dish removed from cart.')
    return redirect(url_for('main.cart'))


@main_bp.route('/decrease_quantity/<int:dish_id>')
@login_required
def decrease_quantity(dish_id):
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == dish_id:
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                cart.remove(item)
            break
    session['cart'] = cart
    return redirect(url_for('main.cart'))


@main_bp.route('/repeat_order/<int:order_id>')
@login_required
def repeat_order(order_id):
    order = Order.query.get_or_404(order_id)
    cart = session.get('cart', [])

    for item in order.items:
        existing = next((c for c in cart if c['id'] == item.dish.id), None)
        if existing:
            existing['quantity'] += item.quantity
        else:
            cart.append({
                'id': item.dish.id,
                'name': item.dish.name,
                'price': item.dish.price,
                'quantity': item.quantity
            })

    session['cart'] = cart
    flash('Order repeated and added to cart.')
    return redirect(url_for('main.cart'))


# Checkout route


@main_bp.route('/checkout')
@login_required
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('main.menu'))

# Create order
    total = sum(item['price'] * item['quantity'] for item in cart)
    order = Order(user_id=current_user.id, total_price=total)
    db.session.add(order)
    db.session.flush()
# Add order items
    for item in cart:
        db.session.add(OrderItem(order_id=order.id,
                                 dish_id=item['id'], quantity=item['quantity']))

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

# Clear cart route


@main_bp.route('/clear_cart')
@login_required
def clear_cart():
    session['cart'] = []
    flash('Cart cleared.')
    return redirect(url_for('main.cart'))
