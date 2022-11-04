from init import db, ma    #< cannot do, because db is in the def
from marshmallow import fields

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    cart_created_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    user = db.relationship('User', back_populates='cart')
    product = db.relationship('Product', back_populates='cart')


class CartSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name'])
    product = fields.List(fields.Nested('ProductSchema', only=['name', 'status', 'price']))
    
    class Meta:
        fields = ('id', 'date', 'product')
        ordered = True