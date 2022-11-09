from flask import Blueprint, request
from init import db
from datetime import date
from models.product import ProductSchema
from models.user import User, UserSchema1
from models.cart import Cart, CartSchema
from controllers.user_controller import authorize1, authorize
from flask_jwt_extended import jwt_required, get_jwt_identity


cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

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
    if not authorize1():
        return {'error': "You do not have authorization."}, 401
    stmt = db.select(User).filter_by(email=email)
    cart = db.session.scalar(stmt)
    if cart:
        return UserSchema1().dump(cart)
    else:
        return {'error': f"Cart not found with {email}."}, 404


#post for adding product to cart
@cart_bp.route('/', methods=['POST'])
@jwt_required()
def create_cart():
    data = ProductSchema().load(request.json)

    cart = Cart(
        product_id = data['id'],
        cart_created_date = date.today(),
        user_id = get_jwt_identity()
    )
    db.session.add(cart)
    db.session.commit()
    return CartSchema().dump(cart), 201


# check each cart by user's email and cart id.
@cart_bp.route('/<string:email>/<int:id>/')
@jwt_required()
def one_cart(email, id):
    stmt = db.select(User).filter_by(email=email)
    stmt = db.select(Cart).filter_by(id=id)
    cart = db.session.scalar(stmt)
    if cart:
        return CartSchema().dump(cart)
    else:
        return {'error': f"Cart not found with id {id}."}, 404

#Delete a cart by user's email and cart id
@cart_bp.route('/<string:email>/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_cart(email, id):
    stmt = db.select(User).filter_by(email=email)
    stmt = db.select(Cart).filter_by(id=id)
    cart = db.session.scalar(stmt)

    if cart:
        db.session.delete(cart)
        db.session.commit()
        return {'message': "Cart deleted successfully."}, 200
    else:
        return {'error': f"Cart not found with id {id}."}, 404
    
