from . import data_base
from flask_login import UserMixin
from sqlalchemy.sql import func  #time

class User(data_base.Model, UserMixin):
    id = data_base.Column(data_base.Integer, primary_key=True)
    name = data_base.Column(data_base.String(20))
    first_name = data_base.Column(data_base.String(30))
    last_name = data_base.Column(data_base.String(30))
    email = data_base.Column(data_base.String(100))
    password = data_base.Column(data_base.String(100))
    notes = data_base.relationship('Note')

class Note(data_base.Model):
    id = data_base.Column(data_base.Integer, primary_key=True)
    note_name = data_base.Column(data_base.String(40))
    text = data_base.Column(data_base.String(10000))
    date = data_base.Column(data_base.DateTime(timezone=True), default=func.now()) # automatically adding time
    user_id = data_base.Column(data_base.Integer, data_base.ForeignKey('user.id'))
