# Online Restaurant

A modular Flask application for managing an online restaurant system.  
Implements authentication, menu management, cart operations, and an admin control panel.  
Uses PostgreSQL through SQLAlchemy ORM and can run both locally and in Docker.

---

## Features

### User side
- Registration and login with Flask-Login and Flask-WTF
- Browsing menu items with images and prices
- Adding, removing, and updating items in the shopping cart
- Order history with full details
- JavaScript-based cart actions without page reloads

### Admin side
- CRUD for dishes (add, edit, delete)
- Order management (status updates, order review)
- Admin-only routes and views
- Basic CSRF and rate-limit protection

---

## Technology Stack

**Language:**  
- Python 3.11

**Framework:**  
- Flask

**Database:**  
- PostgreSQL (connected through SQLAlchemy ORM)  
- SQLite (used locally as fallback)

**Frontend:**  
- HTML5, CSS3, JavaScript (vanilla)

**Styling:**  
- Bootstrap 5  
- Custom CSS (dark theme with green accent)

**Authentication & Forms:**  
- Flask-Login  
- Flask-WTF

**Security:**  
- CSRF protection  
- Session hardening  
- Flask-Limiter (basic rate limiting)

**Containerization:**  
- Docker  
- Docker Compose

---

## Configuration

Application settings are defined in environment variables or in `config.py`.

**Main variables:**
- `SECRET_KEY` — used for Flask session encryption and CSRF tokens  
- `DATABASE_URL` — PostgreSQL connection URI (example: `postgresql://user:password@db:5432/restaurant_db`)  
- `SQLALCHEMY_TRACK_MODIFICATIONS` — disables ORM modification tracking (set to `False` for performance)  
- `DEBUG` — enables Flask debug mode (use `True` only in local development)

**Default local configuration (SQLite):**

`SQLALCHEMY_DATABASE_URI = "sqlite:///restaurant.db"`

## Project Structure

```
online_restaurant/
├── .hintrc
├── Dockerfile
├── README.md
├── app.py
├── config.py
├── docker-compose.yml
├── extensions.py
├── forms/
│   ├── login_form.py
│   ├── menu_form.py
│   ├── order_form.py
│   └── register_form.py
├── generate_structure.py
├── instance/
│   ├── config.py
│   └── restaurant.db
├── models/
│   └── models.py
├── requirements.txt
├── routes/
│   ├── admin.py
│   ├── auth.py
│   └── main.py
├── seed_menu.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   ├── cheesecake.png
│   │   ├── cyber_sushi_set.png
│   │   ├── emerald_pasta.png
│   │   ├── emerald_ramen.png
│   │   ├── forest_soup.png
│   │   ├── neon_tart.png
│   │   ├── shadow_burger.png
│   │   └── shadow_steak.png
│   └── js/
│       ├── animation.js
│       ├── cart_links.js
│       ├── cart_notify.js
│       ├── fadeInCards.js
│       └── notify.js
├── structure.txt
└── templates/
    ├── add_dish.html
    ├── admin.html
    ├── admin_orders.html
    ├── base.html
    ├── cart.html
    ├── edit_dish.html
    ├── index.html
    ├── login.html
    ├── menu.html
    ├── order_history.html
    ├── partials/
    │   └── cart_rows.html
    └── register.html
```

## Local Run
1. Clone repository `git clone https://github.com/yourusername/online-restaurant.git
cd online-restaurant`

2. Create virtual environment

```python -m venv venv
venv\Scripts\activate       # Windows`
or
`source venv/bin/activate   # Linux / macOS
```

3. Install dependencies

`pip install -r requirements.txt`

4. Initialize database (if using SQLite)

```flask shell
>>> from config import db
>>> db.create_all()
>>> exit()
```

5. Run server

`flask run`

Server runs at:

`http://127.0.0.1:5000`

## Run with Docker

1. Build and start containers
`docker-compose up --build`

2. Access

Application → `http://localhost:5000`

PostgreSQL → localhost:5432 (internal container network)

3. Stop containers
`docker-compose down`

## Development Notes

- Modular structure: main, auth, admin blueprints
- Uses SQLAlchemy ORM instead of raw SQL
- Includes CSRF, secure sessions, and basic rate limiting
- Works with SQLite locally, PostgreSQL in Docker
- Static assets stored under static/, templates under templates/

## Possible Improvements

- Password recovery system
- Email notification for order updates
- Admin dashboard charts
- REST API endpoint for external integrations