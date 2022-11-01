from flask import Blueprint
from init import db, bcrypt
from models.user import User




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
    print('Tables Seeded')