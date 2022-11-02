from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.product import Product
from models.cart import Cart
from datetime import date




db_commands = Blueprint('db', __name__) 

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")


# drop all tables
@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables Dropped")


@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name='Admin 01',
            email='admin01@gmail.com',
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            address= 'Company address',
            admin=True
        ),
        User(
            name='Becky L',
            email='BL@gmail.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8'),
            address='1 Abc Street, Brisbane, 4000',
            phone= '0412123123'
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    products = [
        Product(
            categories= 'Food',
            name= 'Royal Canin Gravy Wet Food',
            description= '85g x 12packs, Gravy is tailor made to support the nutritional needs of your growing kitten.',
            price= '30'
        ),
        Product(
            categories= 'Toy',
            name= 'Electronic Floppy Fish',
            description= 'This toy is a great way to encourage your cat or dogs natural urge to play.',
            status= 'Out of stock',
            price= '12'
        ),
        Product(
            categories= 'Litter',
            name= 'Pidan Tofu Cat Litter',
            description= '2.4kg, Comprised of tofu, this litter is the perfect eco-friendly, sustainable, fast clumping, super absorbent option for indoor cats.',
            status= 'Out of Stock',
            price= '19'
        ),
        Product(
            categories= 'Litter',
            name= 'Zodiac Grapefruit Tofu Cat Litter',
            description= '2.5kg, Comprised of tofu, this litter is the perfect eco-friendly, sustainable, fast clumping, super absorbent option for indoor cats.',
            status= 'In Stock',
            price= '14'
        )
    ]
    db.session.add_all(products)
    db.session.commit()

    carts = [
        Cart(
            cart_created_date = date.today(),
            user = users[1],
            product = products[0]
        ),
        Cart(
            cart_created_date = date.today(),
            user = users[0],
            product = products[1]
        )
    ]
    db.session.add_all(carts)
    db.session.commit()

    print('Tables Seeded')