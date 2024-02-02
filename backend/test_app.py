import pytest
from app import app, db, Todo, TestConfig

@pytest.fixture
def client():
    app.config.from_object(TestConfig)
    client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    # Create all tables for the test database
    db.create_all()

    yield client

    # Teardown: Drop the test database
    db.session.remove()
    db.drop_all()
    ctx.pop()

def test_home_page(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"todo_list" in response.data

def test_add_todo_item(client):
    """Test the addition of a new todo item."""
    response = client.post('/add', data=dict(name="Test Todo"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Todo" in response.data

def test_update_todo_item(client):
    """Test the update functionality of a todo item."""
    # Add a test todo item
    new_task = Todo(name="Test Todo", done=False)
    db.session.add(new_task)
    db.session.commit()

    response = client.get(f'/update/{new_task.task_id}', follow_redirects=True)
    assert response.status_code == 200
    updated_task = Todo.query.first()
    assert updated_task.done is True

def test_delete_todo_item(client):
    """Test the delete functionality of a todo item."""
    # Add a test todo item
    new_task = Todo(name="Test Todo", done=False)
    db.session.add(new_task)
    db.session.commit()

    response = client.get(f'/delete/{new_task.task_id}', follow_redirects=True)
    assert response.status_code == 200
    assert Todo.query.count() == 0

def test_about_page(client):
    """Test the about page route."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About" in response.data
