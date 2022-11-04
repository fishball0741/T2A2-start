from flask import Blueprint, request
from init import db
from models.product import Product, ProductSchema

from controllers.user_controller import authorize
from flask_jwt_extended import jwt_required, get_jwt_identity

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


#only admin can do the delete or post
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