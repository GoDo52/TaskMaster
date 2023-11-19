from flask import Flask, render_template


# ======================================================================================================================


app = Flask(__name__)


# ======================================================================================================================


# Should replace with a database later
tasks = [
    {'id': 1, 'title': 'Task 1', 'description': 'This is the first task.'},
    {'id': 2, 'title': 'Task 2', 'description': 'This is the second task.'},
    {'id': 3, 'title': 'Task 2', 'description': 'This is the second task.'},
    {'id': 4, 'title': 'Task 2', 'description': 'This is the second task.'},
    {'id': 5, 'title': 'Task 2', 'description': 'This is the second task.'},
    {'id': 6, 'title': 'Task 2', 'description': 'This is the second task.'},
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks')
def task_list():
    return render_template('task_list.html', tasks=tasks)


@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    # main logic of "adding the task" process
    if request.method == 'POST':
        # whole submission and database logic
        pass
    return render_template('add_task.html')


@app.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # main logic of "editing the task" process
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        if request.method == 'POST':
            # whole submission and database logic
            pass
        return render_template('edit_task.html', task=task)
    else:
        return render_template('task_not_found.html')


# ======================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)
