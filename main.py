from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.user_controller import user_bp


def create_app():
    app = Flask(__name__)


    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)  #using init app to put the app in, split the creation and declaration
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)  #direct the link to bp link
    app.register_blueprint(user_bp)


    # @app.route("/")
    # def hello_world():
    #     return "<p>Hello, World!</p>"

    return app