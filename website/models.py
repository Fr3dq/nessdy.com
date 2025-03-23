from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable = False)
    first_name = db.Column(db.String(150), nullable = False)
    name_surname = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(500), nullable = False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    token = db.Column(db.Integer, nullable = True)
    notes = db.relationship('Note')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(200), nullable = False)
    data = db.Column(db.String(30000), nullable = True)
    spec = db.Column(db.String(600), nullable = True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    username = db.Column(db.String(150), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    links = db.relationship('Links')
    images = db.relationship('Image')

class Links(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(100), nullable = True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(300), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id')) 