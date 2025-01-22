
# TaskMaster

TaskMaster is a simple task manager built using the Python Flask web framework as a personal dummy project.
It allows users to manage their tasks efficiently through a web interface.
It supposed to be hosted on a server or a local computer.

## Features

- Add new tasks
- View existing tasks
- Edit task details
- Delete tasks

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/GoDo52/TaskMaster.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd TaskMaster
   ```

3. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**

   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to:**

   ```
   http://127.0.0.1:5000/
   ```
   or
   ```
   http://your.server.ip.address:5000
   ```

4. **Use the web interface to manage your tasks.**

## Project Structure

```
TaskMaster/
├── static/
│   └── css/
├── templates/
├── .gitignore
├── README.md
├── app.py
├── database.py
└── requirements.txt
```
