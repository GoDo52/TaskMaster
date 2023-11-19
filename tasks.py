from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField


# ======================================================================================================================


class Task:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description


class TaskForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description')


# ======================================================================================================================


def create_task(tasks, title, description):
    new_task = Task(id=len(tasks) + 1, title=title, description=description)
    tasks.append(new_task)
    return new_task


def get_task_by_id(tasks, task_id):
    return next((task for task in tasks if task.id == task_id), None)
