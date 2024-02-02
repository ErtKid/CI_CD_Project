from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app with paths to the template and static directories
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Configure the SQLAlchemy database URI for a MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://utilisateur:mot_de_passe@db/nom_de_la_base_de_donnees'

# Disable the Flask-SQLAlchemy event system for performance reasons
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db = SQLAlchemy(app)

# Configuration class for testing with an in-memory SQLite database
class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

# Define the Todo model with 'task_id', 'name', and 'done' columns
class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean)

# Route to display the home page and list all todo items
@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

# Route to add a new todo item, triggered by a POST request
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")
    new_task = Todo(name=name, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

# Route to update the status of a todo item, identified by 'todo_id'
@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))

# Route to delete a todo item, identified by 'todo_id'
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# Route to display the 'About' page
@app.route('/about')
def about():
    return render_template('about.html')

# Context block to create all database tables upon startup
with app.app_context():
    db.create_all()

# Conditional to only run the Flask app if this script is the main program
if __name__ == '__main__':
    app.run()  # Start the Flask app
