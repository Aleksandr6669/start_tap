from email import message
from sqlite3 import dbapi2
from datetime import datetime
from serverf.init import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_login import UserMixin

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<User %r>' % self.id
    


class Useron(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_on = db.Column(db.String(30), nullable=False)
    ontid = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Messagers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30), nullable=False)
    user_mess = db.Column(db.String(30), nullable=False)
    messager = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Messages %r>' % self.id
    

    

@login_manager.user_loader
def load_user(user):
    return User.query.get(user)


