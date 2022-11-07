from flask import Blueprint, request
from init import db
from datetime import date
from models.product import Product, ProductSchema
from models.user import User, UserSchema1
from models.cart import Cart, CartSchema
from controllers.user_controller import authorize1, authorize
from flask_jwt_extended import jwt_required, get_jwt_identity


cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# def authorize2():
#     user_email = get_jwt_identity()
#     stmt = db.select(User).filter_by(email=user_email)
#     user = db.session.scalar(stmt)
#     return user.email

@cart_bp.route('/')
@jwt_required()
def get_carts():
    if not authorize():
        return {'error': "You do not have authorization."}, 401
    stmt = db.select(Cart)
    carts = db.session.scalars(stmt)
    #trying to set to be only admin can access to see all the users' info.
    return CartSchema(many=True).dump(carts)



@cart_bp.route('/<string:email>/')
@jwt_required()
def one_user_carts(email):
    stmt = db.select(User).filter_by(email=email)
    cart = db.session.scalar(stmt)
    if cart:
        return UserSchema1().dump(cart)
    else:
        return {'error': f"Cart not found with {email}."}, 404


#post for adding stuff to the cart
@cart_bp.route('/', methods=['POST'])
@jwt_required()
def create_cart(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # **********error ****
        cart = Cart(
            user_id = get_jwt_identity(),
            cart = cart,
            cart_created_date = date.today()
        )
    #  Add and commit cart to db
        db.session.add(cart)
        db.session.commit()
        return CartSchema().dump(cart), 201   #dump = out
    else:
        return {'error': f'User not found with id {id}'}, 404


@cart_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_cart(id):
    if not authorize1() == id:
        return {'error': "You do not have authorization."}, 401
    
