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
@cart_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def create_cart(id):
    if not authorize1() == id:
        return {'error': "You do not have authorization."}, 401

    stmt = db.select(Product).filter_by(id=id)  #specify id = id
    cart = db.session.scalar(stmt)

    cart = Product(
        categories = request.json['categories'],
        name = request.json['name'],
        description = request.json.get('description'),
        status = request.json.get('status'),
        price = request.json['price'],
        user_id = get_jwt_identity()
        # categories = request.json.get('categories') or product.categories,
        # name = request.json.get('name') or product.name,
        # description = request.json.get('description') or product.description,
        # status = request.json.get('status') or product.status,
        # price = request.json.get('price') or product.price,
        # user_id = get_jwt_identity()
    )
        # **********error ****
        # cart = Cart(
        #     product = request.json.get('product'),
        #     cart_created_date = date.today(),
        #     user_id = get_jwt_identity()
        # )
        
        
    #  Add and commit cart to db
    db.session.add(cart)
    db.session.commit()
    return CartSchema().dump(cart), 201   #dump = out


@cart_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_cart(id):
    if not authorize1() == id:
        return {'error': "You do not have authorization."}, 401
    
