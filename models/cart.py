from init import db, ma    #< cannot do, because db is in the def
from marshmallow import fields

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    cart_created_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    user = db.relationship('User', back_populates='cart')
    # add = db.relationship('Add', back_populates='cart', cascade='all, delete')
    product = db.relationship('Product', back_populates='cart')


class CartSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['email'])
    # add = fields.List(fields.Nested('AddSchema'))
    product = fields.Nested('ProductSchema')

    
    class Meta:
        fields = ('user', 'cart_created_date', 'product')   # no add first.
        ordered = True


