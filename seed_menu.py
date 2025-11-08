from app import app
from extensions import db
from models.models import Dish

with app.app_context():
    demo_dishes = [
        Dish(
            name="Emerald Pasta",
            description="Fresh spinach tagliatelle in creamy basil sauce with hints of garlic and lemon.",
            price=12.50,
            image_url="/static/images/emerald_pasta.png"
        ),
        Dish(
            name="Cyber Sushi Set",
            description="Neon-bright rolls of salmon, avocado, and wasabi, crafted with precision.",
            price=15.00,
            image_url="/static/images/cyber_sushi_set.png"
        ),
        Dish(
            name="Shadow Burger",
            description="Black-bun beef burger with jalapeños, melted cheddar, and secret green aioli.",
            price=13.20,
            image_url="/static/images/shadow_burger.png"
        ),
        Dish(
            name="Forest Soup",
            description="Creamy mushroom soup with truffle oil, served with herb-crusted bread.",
            price=9.80,
            image_url="/static/images/forest_soup.png"
        ),
        Dish(
            name="Green Tea Cheesecake",
            description="Velvety matcha cheesecake on crispy almond base — smooth and vibrant.",
            price=7.50,
            image_url="https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80"
        ),

        Dish(
            name="Shadow Steak",
            description="Charcoal-grilled ribeye glazed with black garlic butter.",
            price=24.50,
            image_url="/static/images/shadow_steak.png"
        ),
        Dish(
            name="Emerald Ramen",
            description="Deep green matcha-infused broth with soba noodles and poached egg.",
            price=15.20,
            image_url="/static/images/emerald_ramen.png"
        ),

        Dish(
            name="Neon Tart",
            description="Dark chocolate tart topped with glowing mint crystals.",
            price=8.90,
            image_url="/static/images/neon_tart.png"
        ),]

    db.session.add_all(demo_dishes)
    db.session.commit()
    print("✅ Menu populated with demo dishes.")
