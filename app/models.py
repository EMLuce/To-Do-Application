'''Utilized to manipulate the back-end of all authentication views.'''
from flask_login import UserMixin
from app import db
from . import *

app = create_app

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Note')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.String(150))
    due_date = db.Column(db.String(150))
    note = db.Column(db.String(1000))
    completed = db.Column(db.Boolean, default=False, server_default="false")
    completed_date = db.Column(db.String(150), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
