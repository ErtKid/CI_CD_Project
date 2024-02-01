import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, Todo

import sys
sys.path.insert(0, 'backend')

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Todo App', response.data)

    def test_add_route(self):
        response = self.app.post('/add', data={'name': 'Task 1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.query.count(), 1)

    def test_update_route(self):
        todo = Todo(name='Task 1', done=False)
        db.session.add(todo)
        db.session.commit()
        response = self.app.get(f'/update/{todo.task_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update Task', response.data)

    def test_delete_route(self):
        todo = Todo(name='Task 1', done=False)
        db.session.add(todo)
        db.session.commit()
        response = self.app.get(f'/delete/{todo.task_id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.query.count(), 0)

    def test_about_route(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

if __name__ == '__main__':
    unittest.main()
