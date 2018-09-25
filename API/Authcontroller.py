from flask import Flask, request, jsonify, make_response, Blueprint
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps 
import jwt
import token
import datetime
from .Model.Model import User, db
from . import app
bp = Blueprint('auth', __name__)


#Decorator
def token(f):
    @wraps(f)
    def decorator_function(*args, **Kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message' : 'token is missing'})
        try:
            data = jwt.decode(token, app.config ['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token invalid'})
        return f(current_user, *args, **Kwargs)
    return decorator_function

@bp.route('/login', methods = ['POST'])
def login():
    auth = request.get_json()
    user = User.query.filter_by(email=auth['email']).first()
    if not user:
        return jsonify({'message' : 'Error'})
    else:
        if check_password_hash(user.password, auth['password']):
            token = jwt.encode({'id':user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('utf-8')})
        else:
            return jsonify({'message' :'wrong email or password'})
        

@bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, admin=True)
    try: 
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message' : 'User created'})
        else:
            return jsonify({'Error user not created'})
    except sqlalchemy.exc.IntegrityError: 
        return jsonify({'message' : 'User already exist'}), 401


@token        
@bp.route('/logout') 
def logout():
    if 'token' in request.headers:
        token = None
        return jsonify({'message':'logout'})
        


