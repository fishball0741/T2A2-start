from init import db, ma    #< cannot do, because db is in the def
from marshmallow import fields




class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)  #false mean cannot null, must write the email.   unique = only can register one
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer)
    admin = db.Column(db.Boolean, default=False)   #admin had authorization, so no default.

    product = db.relationship('Product', back_populates='users')
    cart = db.relationship('Cart',back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    product = fields.List(fields.Nested('ProductSchema'))
    cart = fields.Nested('CartSchema')


    class Meta:
        fields = ('id', 'name', 'email', 'password', 'address', 'phone', 'admin', 'cart')   # know we need password but not it json.