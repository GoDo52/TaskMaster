from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


# ======================================================================================================================


db = SQLAlchemy()


# ======================================================================================================================


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)


# ======================================================================================================================


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, description, user):
        self.title = title
        self.description = description
        self.user = user


class TaskForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description')


# ======================================================================================================================
