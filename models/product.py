from unicodedata import category
from wsgiref import validate
from init import db, ma    #< cannot do, because db is in the def
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError


VALID_CATEGORIES = ('Food', 'Toy', 'Litter')
VALID_STATUSES = ('In Stock', 'Out of Stock')

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    categories = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String, default=VALID_STATUSES[0])
    price = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    users = db.relationship('User',back_populates='product')

    cart = db.relationship('Cart',back_populates='product', cascade='all, delete')
    # #if product deleted, cart can't function



class ProductSchema(ma.Schema):
    users = fields.Nested('UserSchema', only=['name'])
    cart = fields.Nested('CartSchema')


    class Meta:
        fields = ('id', 'categories', 'name', 'description', 'status', 'price') 

        ordered = True