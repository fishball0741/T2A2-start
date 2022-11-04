from flask import Blueprint, request
from init import db
from datetime import date
from models.product import Product, ProductSchema
from models.cart import Cart, CartSchema
from controllers.user_controller import authorize
from flask_jwt_extended import jwt_required, get_jwt_identity


cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

#post for adding stuff to the cart
@cart_bp.route('/', methods=['POST'])
@jwt_required()
def create_cart():
    data = CartSchema().load(request.json)   #load from the schema is apply the validation from the Schema
    cart = Cart(
        cart_created_date = date.today(),
        user = data['name'],
    )
    #  Add and commit card to db
    db.session.add(cart)
    db.session.commit()
    return CartSchema().dump(cart), 201   #dump = out


@cart_bp.route('/')
@jwt_required()
def get_carts():
    stmt = db.select(Cart)
    carts = db.session.scalars(stmt)

    return CartSchema(many=True).dump(carts)