from app import app, db
from models.models import Dish

with app.app_context():
    dishes = [
        Dish(name='Pizza Margherita',
             description='Classic pizza with mozzarella and tomato sauce', price=8.5),
        Dish(name='Pasta Carbonara',
             description='Pasta with creamy sauce and bacon', price=10.0),
        Dish(name='Tiramisu', description='Traditional Italian dessert', price=5.5)
    ]

    db.session.add_all(dishes)
    db.session.commit()
    print('Dishes added successfully!')
