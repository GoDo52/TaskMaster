import secrets

from flask import Flask, render_template, request, redirect, url_for

from tasks import Task, create_task, get_task_by_id, TaskForm


# ======================================================================================================================


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# ======================================================================================================================


# Should replace with a database later
tasks = [
    Task(1, 'Task 1', 'This is the first task.'),
    Task(2, 'Task 2', 'This is the second task.'),
    Task(3, 'Task 3', 'This is the third task.'),
    Task(4, 'Task 4', 'This is the fourth task.'),
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks')
def task_list():
    return render_template('task_list.html', tasks=tasks)


@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        # remake for adding to database later
        new_task = create_task(tasks, form.title.data, form.description.data)
        return redirect(url_for('task_list'))
    return render_template('add_task.html', form=form)


@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_task_by_id(tasks, task_id)
    if task:
        form = TaskForm(obj=task)
        if form.validate_on_submit():
            # remake for updating in database later
            task.title = form.title.data
            task.description = form.description.data
            return redirect(url_for('task_list'))
        return render_template('edit_task.html', task=task, form=form)
    else:
        return render_template('task_not_found.html')


# ======================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)
