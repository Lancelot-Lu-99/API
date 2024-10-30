from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'testonlyfornow'  # use secret key to replace'testonlyfornow'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5703@localhost:5432/5703' # postgresql://username:userpassword@localhost:5432/databasename
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt.init_app(app)
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
