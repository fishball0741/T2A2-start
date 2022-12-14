from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required



user_bp = Blueprint('user', __name__, url_prefix='/user')


def authorize():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.admin

def authorize1():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.id
    


#only for admin can see all users' info
@user_bp.route('/')
@jwt_required()
def get_users():
    if not authorize():
        return {'error': "You do not have authorization."}, 401
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    #trying to set to be only admin can access to see all the users' info.
    return UserSchema(many=True).dump(users)


#only for user who see their own info.
@user_bp.route('/<int:id>/')
@jwt_required()
def one_user(id):
    if not authorize1() == id:
        return {'error': "You do not have authorization."}, 401
        
    stmt = db.select(User).filter_by(id=id)  #specify id = id
    user = db.session.scalar(stmt)
    if user:
        return UserSchema().dump(user)
    else:
        return {'error': f"User not found with id {id}."}, 404

#for user to register
@user_bp.route('/register/', methods=['POST'])
def user_register():
    try:
        user = User(
            name = request.json['name'],
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
            address = request.json['address'],
        )
        db.session.add(user)
        db.session.commit()

        return UserSchema().dump(user), 201

    except IntegrityError:
        return {'error': 'Email address already in use'}, 409


#for user to login
@user_bp.route('/login/', methods=['POST'])
def user_login():
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))
        return {'email': user.email, 'token': token, 'id': user.id, 'admin': user.admin}

    else:
        return {'error': 'Invalid password or email'}, 401

