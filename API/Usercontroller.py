from flask import Flask, request, jsonify, make_response, Blueprint, flash
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .Model.Model import db, User
from .Authcontroller import token
bp = Blueprint('user', __name__)

@bp.route('/create/user', methods=['POST'])
@token
def create_user(current_user):
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


@bp.route('/get/user', methods=['GET'])
@token
def get_user(current_user):
    users = User.query.all()
    result = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        result.append(user_data)
    
    return jsonify(result) 

@bp.route('/edit/user/<id>', methods=['PUT'])
@token
def edit_user_id(current_user, id):
    user = User.query.filter_by(id=int(id)).first()
    data = request.get_json()

    user.name = data['name']
    user.email = data['email']
    user.password = data['password']
    user.admin = True
    db.session.add(user)
    db.session.commit()

    return jsonify({'message':'User modified'}) 

@bp.route('/delete/user/<id>', methods=['DELETE'])
@token
def delete_user_id(current_user, id):
    user = User.query.filter_by(id=int(id)).first()
   
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message':'User Deleted'}) 