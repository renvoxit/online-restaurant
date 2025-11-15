from extensions import db
from models.models import Dish


def seed_menu():
    """Populate the menu with demo dishes if it's empty."""

    if Dish.query.first():
        return  # menu already exists — do nothing

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
            image_url="/static/images/cheesecake.png"
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
        ),
    ]

    db.session.add_all(demo_dishes)
    db.session.commit()
    print("Menu seeded.")
