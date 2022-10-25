import os
from flask import Flask
from db import db, ma
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from controllers.cards_controller import cards_bp
# from models.card import Card

# db = SQLAlchemy() # now db is funciton not the module
# ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    
    @app.errorhandler(404)
    def not_found(err):
        # return {'error': err.description}, 404
        return {'error': str(err)}, 404

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)
    ma.init_app(app)
    
    
    # @app.route('/')
    # def index():
    #     return 'Hello!!!!'

    app.register_blueprint(cards_bp)
    
    return app



