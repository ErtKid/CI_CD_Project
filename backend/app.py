from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://utilisateur:mot_de_passe@db/nom_de_la_base_de_donnees'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app, version='1.0', title='Todo API', description='A simple Todo API')

# Définition du modèle pour la documentation OpenAPI
todo_model = api.model('Todo', {
    'task_id': fields.Integer(readonly=True, description='The task unique identifier'),
    'name': fields.String(required=True, description='The task details'),
    'done': fields.Boolean(description='The status of the task')
})

# Classe pour le modèle SQLAlchemy
class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean)

# Resource pour la liste de todos
@api.route('/api/todos')
class TodoList(Resource):
    @api.marshal_list_with(todo_model)
    def get(self):
        '''List all tasks'''
        return Todo.query.all()

    @api.expect(todo_model)
    def post(self):
        '''Create a new task'''
        data = request.json
        new_task = Todo(name=data['name'], done=False)
        db.session.add(new_task)
        db.session.commit()
        return {'task_id': new_task.task_id, 'name': new_task.name, 'done': new_task.done}, 201

# Resource pour une tâche unique
@api.route('/api/todos/<int:id>')
@api.response(404, 'Todo not found')
@api.param('id', 'The task identifier')
class TodoItem(Resource):
    @api.marshal_with(todo_model)
    def get(self, id):
        '''Fetch a given resource'''
        todo = Todo.query.get_or_404(id)
        return todo

    @api.expect(todo_model)
    def put(self, id):
        '''Update a task given its identifier'''
        todo = Todo.query.get_or_404(id)
        data = request.json
        todo.name = data.get('name', todo.name)
        todo.done = data.get('done', todo.done)
        db.session.commit()
        return todo

    @api.response(204, 'Todo successfully deleted.')
    def delete(self, id):
        '''Delete a task given its identifier'''
        todo = Todo.query.get_or_404(id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

# Les routes Flask classiques restent inchangées
@app.route('/')
def home():
    return render_template('index.html', todo_list=Todo.query.all())

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
