from flask import jsonify, render_template_string
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


@main_bp.route('/add_to_cart/<int:dish_id>', methods=['POST'])
@login_required
def add_to_cart(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    cart = session.get('cart', [])
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
            'image_url': getattr(dish, 'image_url', None),
        })
    session['cart'] = cart

    html = render_template('partials/cart_rows.html', cart_items=cart)
    total = sum(i['price'] * i['quantity'] for i in cart)
    return jsonify({'html': html, 'total': f'{total:.2f}'})
# Remove from cart route


@main_bp.route('/remove_from_cart/<int:dish_id>', methods=['POST'])
@login_required
def remove_from_cart(dish_id):
    cart = [i for i in session.get('cart', []) if i['id'] != dish_id]
    session['cart'] = cart

    html = render_template('partials/cart_rows.html', cart_items=cart)
    total = sum(i['price'] * i['quantity'] for i in cart)
    return jsonify({'html': html, 'total': f'{total:.2f}'})


@main_bp.route('/decrease_quantity/<int:dish_id>', methods=['POST'])
@login_required
def decrease_quantity(dish_id):
    cart = session.get('cart', [])
    for idx, item in enumerate(cart):
        if item['id'] == dish_id:
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                cart.pop(idx)
            break
    session['cart'] = cart

    html = render_template('partials/cart_rows.html', cart_items=cart)
    total = sum(i['price'] * i['quantity'] for i in cart)
    return jsonify({'html': html, 'total': f'{total:.2f}'})


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


# Cancel order
@main_bp.route('/cancel_order/<int:order_id>')
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash("You can only cancel your own orders.")
        return redirect(url_for('main.orders'))

    if order.status not in ["Delivered", "Cancelled"]:
        order.status = "Cancelled"
        db.session.commit()
        flash(f"Order #{order.id} has been cancelled.")
    else:
        flash(f"Order #{order.id} cannot be cancelled.")

    return redirect(url_for('main.orders'))


# Repeat order (reworked version — safer merge into cart)
@main_bp.route('/repeat_order/<int:order_id>')
@login_required
def repeat_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash("You can only repeat your own orders.")
        return redirect(url_for('main.orders'))

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
    flash(f"Order #{order.id} items added to cart.")
    return redirect(url_for('main.cart'))


# Clear cart route
@main_bp.route('/clear_cart')
@login_required
def clear_cart():
    session['cart'] = []
    flash('Cart cleared.')
    return redirect(url_for('main.cart'))


@main_bp.route("/__fix_render_once__", methods=["GET"])
def fix_render_once():
    from extensions import db
    from models.models import User, Dish
    from seed_menu import seed

    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", email="admin@example.com")
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()

    dishes = Dish.query.all()
    if not dishes:
        seed()

    return "Render FIXED: admin + menu ready."
