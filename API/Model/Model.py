from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from ..settings import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    value = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

db.create_all()