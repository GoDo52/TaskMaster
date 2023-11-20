import secrets

from flask import Flask, render_template, request, redirect, url_for

from tasks import Task, TaskForm, db


# ======================================================================================================================


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    # there goes your credentials for AWS RDS
    admin = ""
    password = ""
    host = ""
    port = ""
    database = ""
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{admin}:{password}@{host}:{port}/{database}'
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


app = create_app()


# ======================================================================================================================


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks')
def task_list():
    tasks = Task.query.all()
    return render_template('task_list.html', tasks=tasks)


@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('task_list'))
    return render_template('add_task.html', form=form)


@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task:
        form = TaskForm(obj=task)
        if form.validate_on_submit():
            task.title = form.title.data
            task.description = form.description.data
            db.session.commit()
            return redirect(url_for('task_list'))
        return render_template('edit_task.html', task=task, form=form)
    else:
        return render_template('task_not_found.html')


# ======================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)
