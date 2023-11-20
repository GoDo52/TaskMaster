import secrets

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
    admin = "admin"
    password = "adminadmin"
    host = "taskmanager.cywfs8sp5cgm.eu-north-1.rds.amazonaws.com"
    port = "3306"
    database = "taskmanagerdb"
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


# ======================================================================================================================


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

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
    tasks = Task.query.all()
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


if __name__ == '__main__':
    app.run(debug=True)
