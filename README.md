# Online Restaurant

Online Restaurant is a web application built with Flask and SQLAlchemy, simulating a modern online restaurant:
users can register, log in, browse the menu, place and manage their orders, while the administrator controls the menu and order statuses.

***

## Tech Stack

- Python 3.13+
- Flask — web framework
- Flask-Login — authentication and session management
- Flask-WTF / CSRFProtect — form validation and security
- Flask-SQLAlchemy — ORM database layer
- Flask-Limiter — request rate limiting
- Bootstrap 5 — responsive layout and styling
- SQLite / PostgreSQL — database backend

## Project Structure

```online_restaurant/
│
├── app.py                     # Entry point — creates Flask app, registers blueprints
├── config.py                  # Core configuration (Config class, db initialization)
├── requirements.txt           # Project dependencies
│
├── instance/
│   └── config.py              # Local development config (SECRET_KEY, DEBUG, SQLite)
│
├── models/
│   └── models.py              # Database models: User, Dish, Order, OrderItem
│
├── routes/
│   ├── auth.py                # Registration, login, logout
│   ├── main.py                # Menu, cart, checkout, order history
│   └── admin.py               # Admin panel — manage dishes and orders
│
├── forms/
│   ├── login_form.py          # Flask-WTF login form
│   ├── register_form.py       # Flask-WTF registration form
│   ├── menu_form.py           # (reserved for future menu features)
│   └── order_form.py          # (reserved for future order extensions)
│
├── templates/
│   ├── base.html              # Shared layout with header & flash messages
│   ├── index.html             # Home page
│   ├── login.html             # Login form
│   ├── register.html          # Registration form
│   ├── menu.html              # Menu list with “Add to cart”
│   ├── cart.html              # Shopping cart
│   ├── order_history.html     # User order history
│   ├── admin.html             # Admin panel (add/delete dishes)
│   ├── edit_dish.html         # Edit dish form
│   └── admin_orders.html      # All orders overview + status update
│
└── static/
    ├── css/                   # Stylesheets
    ├── js/                    # Scripts
    └── images/                # Dish images
```

## Features
### User

- Register and log in
- View menu and add dishes to cart
- Modify or remove items in the cart
- Place orders
- View order history
- Repeat or cancel past orders

---

### Administrator

- Add new dishes to the menu
- Edit or delete existing dishes
- View all orders
- Change order statuses (Pending → Preparing → Delivered → Cancelled)

## Configuration

```Local config (instance/config.py):
SECRET_KEY = "local_dev_secret"
SQLALCHEMY_DATABASE_URI = "sqlite:///restaurant.db"
DEBUG = True
WTF_CSRF_ENABLED = True
```

## How to Run

Create a virtual environment

```python -m venv venv
source venv/bin/activate       # Linux / Mac
venv\Scripts\activate          # Windows
```
Install dependencies

`pip install -r requirements.txt`

Run the application
`flask run`
or
`python app.py`

Open in browser:
http://127.0.0.1:5000

## Database

Automatically created on first run as restaurant.db
To use PostgreSQL, update in instance/config.py:

`SQLALCHEMY_DATABASE_URI = "postgresql://user:password@host:port/dbname"`

## Security

- All POST forms include CSRF tokens
- Passwords hashed via werkzeug.security
- Secure cookies: HttpOnly, SameSite=Lax
- Rate limiting active: 10 POST requests / minute

## Deployment

When deploying to a production server:

```SESSION_COOKIE_SECURE = True
WTF_CSRF_SSL_STRICT = True
```
and set environment variables:

```DATABASE_URL="postgresql://user:password@host:port/dbname"
SECRET_KEY="your_production_secret"
```
