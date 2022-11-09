from flask import Blueprint, request
from init import db
from models.product import Product, ProductSchema
from controllers.user_controller import authorize
from flask_jwt_extended import jwt_required

product_bp = Blueprint('product', __name__, url_prefix='/product')

#no jwt required, because anyone can assess to look the product
@product_bp.route('/')
def all_products():

    # asc or desc (for status), showing the in-stock first.
    stmt = db.select(Product).order_by(Product.status.asc(), Product.categories.asc(), Product.name)
    product = db.session.scalars(stmt)
    return ProductSchema(many=True).dump(product)

@product_bp.route('/<int:id>/')
def one_product(id):
    stmt = db.select(Product).filter_by(id=id)
    product = db.session.scalar(stmt)
    if product:
        return ProductSchema().dump(product)
    else:
        return {'error': f"Product not found with id {id}."}, 404


#only admin can do the delete
@product_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_product(id):
    if not authorize():
        return {'error': "You do not have authorization."}, 401

    stmt = db.select(Product).filter_by(id=id)
    product = db.session.scalar(stmt)

    if product:
        db.session.delete(product)
        db.session.commit()
        return {'message': f"Product '{product.name}' deleted successfully."}, 200
    else:
        return {'error': f"Product not found with id {id}."}, 404


#only admin can do the update  (eg. change price, change status)
@product_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_product(id):
    if not authorize():
        return {'error': "You do not have authorization."}, 401
    stmt = db.select(Product).filter_by(id=id)  #specify id = id
    product = db.session.scalar(stmt)  # single product, single scalar
    if product:
        # json.get = get = return none if it's not excits, means no error
        # but make sure change [ ]  to ( ) instead.
        product.categories = request.json.get('categories') or product.categories
        product.name = request.json.get('name') or product.name   #means, if the new update not success, will put the previous one
        product.description = request.json.get('description') or product.description
        product.status = request.json.get('status') or product.status
        product.price = request.json.get('price') or product.price
        db.session.commit()  #commit = update the data
        return ProductSchema().dump(product)
    else:
        return {'error': f"Product not found with id {id}."}, 404


#only admin can do the post (post new product)
@product_bp.route('/', methods=['POST'])   
@jwt_required()
def create_product():
    if not authorize():
        return {'error': "You do not have authorization."}, 401
    # Create a new product model instance
    data = ProductSchema().load(request.json)   #load from the schema is apply the validation from the Schema
    product = Product(
        categories = data['categories'],
        name = data['name'],
        description = data.get('description'),
        status = data.get('status'),
        price = data['price'],
    )
    #  Add and commit cart to db
    db.session.add(product)
    db.session.commit()
    return ProductSchema().dump(product), 201   #dump = out


