from flask import Flask, request, jsonify, make_response, Blueprint
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps 
import jwt
import token
import datetime
from .Model.Model import User, db, Alert
from . import app
from .Authcontroller import token
bp = Blueprint('alert', __name__)

@bp.route('/create/alert', methods=['POST'])
@token
def create_alert(current_user):
    data = request.get_json()
    new_alert = Alert(text=data['text'], value=data['value'], user_id=current_user.id, active=True)
    try: 
        if new_alert:
            db.session.add(new_alert)
            db.session.commit()
            return jsonify({'message' : 'Alert created'})
        else:
            return jsonify({'Error Alert not created'})
    except sqlalchemy.exc.IntegrityError: 
        return jsonify({'message' : 'Alert already exist'}), 401

@bp.route('/get/alert', methods=['GET'])
@token
def get_alert(current_user):
    alerts = Alert.query.all()
    result = []
    for alert in alerts:
        alert_data = {}
        alert_data['id'] = alert.id
        alert_data['text'] = alert.text
        alert_data['value'] = alert.value
        alert_data['active'] = alert.active
        alert_data['user_id'] = alert.user_id
        result.append(alert_data)
    
    return jsonify(result)  

@bp.route('/edit/alert/<id>', methods=['PUT'])
@token
def edit_alert_id(current_user, id):
    alert = Alert.query.filter_by(id=int(id)).first()
    data = request.get_json()

    alert.text = data['text']
    alert.value = data['value']
    alert.active = True 
    db.session.add(alert)
    db.session.commit()

    return jsonify({'message':'Alert modified'}) 

@bp.route('/delete/alert/<id>', methods=['DELETE'])
@token
def delete_alert_id(current_user, id):
    alert = Alert.query.filter_by(id=int(id)).first()
   
    db.session.delete(alert)
    db.session.commit()

    return jsonify({'message':'Alert Deleted'}) 