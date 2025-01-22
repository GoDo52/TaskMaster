import secrets
import boto3

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

from database import Task, TaskForm, User, db


# ======================================================================================================================


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    # there goes your credentials for AWS RDS
    ssm = boto3.client('ssm', region_name='Europe')

    admin = ssm.get_parameter(Name='/TaskManager/db_username', WithDecryption=True)['Parameter']['Value']
    password = ssm.get_parameter(Name='/TaskManager/db_password', WithDecryption=True)['Parameter']['Value']
    host = ssm.get_parameter(Name='/TaskManager/db_host')['Parameter']['Value']
    port = ssm.get_parameter(Name='/TaskManager/db_port')['Parameter']['Value']
    database = ssm.get_parameter(Name='/TaskManager/db_name')['Parameter']['Value']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{admin}:{password}@{host}:{port}/{database}'
    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    return app


app = create_app()


# ======================================================================================================================


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class DuplicateUserError(Exception):
    pass


# ======================================================================================================================


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('task_list'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/tasks')
@login_required
def task_list():
    tasks = current_user.tasks
    return render_template('task_list.html', tasks=tasks)


@app.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        new_task = Task(title=title, description=description, user=current_user)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('task_list'))
    return render_template('add_task.html', form=form)


@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
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


@app.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user == current_user:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('task_list'))
    else:
        return render_template('task_not_found.html')


# ======================================================================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(403)
def access_denied(e):
    return render_template('403.html'), 403

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


# ======================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)
