from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.card import Card, CardSchema
from controllers.auth_controller import authorize
from init import db

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
# @jwt_required()
def get_all_cards():
    # if not authorize():
    #     return {'error': 'You must be an admin'}, 401
    
    stmt = db.select(Card).order_by(Card.id.asc(), Card.title)
    cards = db.session.scalars(stmt)
    return CardSchema(many=True).dump(cards)
    # return 'all_cards route'
    
@cards_bp.route('/<int:id>/') #called RESTful parameters, 보통 파라미터는 string이여서 따로 int라는 겻을 명시해줬다.
def get_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return {'error': f'Card not found with id {id}'}, 404
    
@cards_bp.route('/<int:id>/', methods=['DELETE']) #called RESTful parameters, 보통 파라미터는 string이여서 따로 int라는 겻을 명시해줬다.
@jwt_required()
def delete_one_card(id):
    authorize()
    # if not authorize():
    #     return {'error': 'You must be an admin'}, 401

    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return {'message': f'Card "{card.title}" deleted successfully'}
    else:
        return {'error': f'Card not found with id {id}'}, 404
    
@cards_bp.route('/<int:id>/', methods=['PUT', 'PATCH']) # patch means partially update opposite meaning is PUT
@jwt_required()
def update_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        card.title = request.json.get('title') or card.title  # []와 get() 차이점 
        card.description = request.json.get('description') or card.description
        card.status = request.json.get('status') or card.status,
        card.priority = request.json.get('priority') or card.priority
        db.session.commit() # we don't need to add because we already have
        return CardSchema().dump(card)
    else:
        return {'error': f'Card not found with id {id}'}, 404

@cards_bp.route('/', methods=['POST'])
@jwt_required()
def create_card(): # this called Handler funciton
    # try:
        # Create a new card model instance
    card = Card(
        title = request.json['title'],
        description = request.json['description'],
        date = date.today(),
        status = request.json['status'],
        priority = request.json['priority'],
    )
    # Add and commit user to DB
    db.session.add(card)
    db.session.commit()
    # Respond to client 
    return CardSchema().dump(card), 201
    # except IntegrityError:
        # return {'error': 'Email address already in use'}, 409