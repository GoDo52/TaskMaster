from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_sqlalchemy import SQLAlchemy


# ======================================================================================================================


db = SQLAlchemy()


# ======================================================================================================================


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    def __init__(self, title, description):
        self.title = title
        self.description = description


class TaskForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description')


# ======================================================================================================================
