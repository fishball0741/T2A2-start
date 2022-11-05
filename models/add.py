from init import db, ma    #< cannot do, because db is in the def
from marshmallow import fields


class Add(db.Model):  
    __tablename__ = 'add'

    id = db.Column(db.Integer, primary_key=True) 

    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    cart = db.relationship('Cart', back_populates='add')
    product = db.relationship('Product', back_populates='add')

    


class AddSchema(ma.Schema):
    cart = fields.Nested('CartSchema')
    product = fields.List(fields.Nested('ProductSchema', only=['name', 'status', 'price']))
    
    class Meta:
        fields = ('id', 'cart', 'product')
        ordered = True
