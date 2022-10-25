from datetime import timedelta
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity
from init import db, bcrypt
from models.user import User, UserSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try:
        #Load the posted user info and parse the JSON
        # user_info = UserSchema().load(request.json)
        #create a new User model instance from the user_info
        user = User(
            email= request.json['email'],
            password=bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
            name=request.json.get('name')
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Resp[ond to client]
        # print(request.json)
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError: 
        return {'error': 'Email address already in use'}, 409

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # print(request.json)
    #  Find a user by email address
    stmt = db.select(User).filter_by( email=request.json['email'] )
    # stmt = db.select(User).where( User.email == request.json['email'] )
    # print(stmt.compile().params)
    user = db.session.scalar(stmt)  

    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # return UserSchema(exclude=['password']).dump(user)
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or  password'}, 401
      
def authorize():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)
    # return user.is_admin