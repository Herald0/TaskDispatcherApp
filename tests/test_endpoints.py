import time
from datetime import datetime
import pytest

from app.db.models import User, Task
from httpx import AsyncClient, ASGITransport

from app.db.database import get_async_session
from main import app


# TEST_USERS


@pytest.fixture()
def override_db_session():
    async def override_get_async_session():
        class FakeScalarResult:
            def all(self):
                return [User(username='n', email='n@gmail.com', password='123')]

        class FakeResult:
            def scalars(self):
                return FakeScalarResult()

        class FakeSession:
            async def execute(self, statement):
                return FakeResult()

        yield FakeSession()

    app.dependency_overrides[get_async_session] = override_get_async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)

@pytest.fixture
def override_db_session_no_user():
    async def override_get_async_session():
        class FakeScalarResult:
            def all(self):
                return []
        
        class FakeResult:
            def scalars(self):
                return FakeScalarResult()
        
        class FakeSession:
            async def execute(self, statement):
                return FakeResult()
            
            def add(self, obj):
                pass
            
            async def commit(self):
                pass
            
            async def refresh(self, obj):
                obj.id = 1
                obj.created_at = datetime.now()

        yield FakeSession()
    
    app.dependency_overrides[get_async_session] = override_get_async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client

@pytest.mark.anyio
async def test_protected_endpoint_failed(client):
    response = await client.get('/join_table')
    assert response.status_code == 401

@pytest.mark.anyio
async def test_protected_endpoint(override_db_session, client):
    response = await client.post(
        '/users/login',
        json={'username': 'n', 'password': '123'}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data

    response = await client.get(
        '/join_table',
        headers={'Authorization': f'Bearer {data["access_token"]}'}
    )
    assert response.status_code == 200

    response = await client.get(
        '/join_table',
        headers={'Authorization': f'Bearer {'fesge' + data["access_token"]}'}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid token'}

@pytest.mark.anyio
async def test_register_already_exists(override_db_session, client):
    response = await client.post(
        '/users/',
        json={'username': 'n', 'email': 'n@gmail.com', 'password': '123'}
    )
    assert response.status_code == 401
    data = response.json()
    assert data['detail'] == {'message': 'User already exists'}

@pytest.mark.anyio
async def test_register(override_db_session_no_user, client):
    response = await client.post(
        '/users/',
        json={'username': 'n', 'email': 'n@gmail.com', 'password': '123'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == 'n'
    assert data['email'] == 'n@gmail.com'
    assert data['password'] == '123'


# TEST_TASKS


@pytest.fixture()
def override_db_session_tasks():
    async def override_get_async_session():
        class FakeScalarsResult:
            def all(self):
                return [
                    Task(
                        id=1,
                        title='t1',
                        description='d1',
                        completed=False,
                        created_at=datetime.now(),
                    )
                ]
            
        class FakeResult:
            def scalars(self):
                return FakeScalarsResult()

        class FakeSession:
            async def execute(self, statement):
                return FakeResult()

        yield FakeSession()
    
    app.dependency_overrides[get_async_session] = override_get_async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)

@pytest.mark.anyio
async def test_get_tasks(override_db_session_tasks, client):
    result = await client.get('/tasks/')
    assert result.status_code == 200
    data = result.json()
    assert data[0]['title'] == 't1'
    assert data[0]['description'] == 'd1'
    assert data[0]['completed'] == False

@pytest.mark.anyio
async def test_create_task(override_db_session_no_user, client):
    response = await client.post(
        '/tasks/',
        json={'title': 't1', 'description': 'd1'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 't1'
    assert data['description'] == 'd1'
    assert data['completed'] == False
    assert data['id'] == 1

@pytest.fixture()
def override_db_session_change_task():
    async def override_get_async_session():
        class FakeSession:
            async def get(self, s1, s2):
                return Task(id=1, title='t1', description='d1', completed=False, created_at=datetime.now())

            async def commit(self):
                pass

        yield FakeSession()
    
    app.dependency_overrides[get_async_session] = override_get_async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)

@pytest.mark.anyio
async def test_change_task(override_db_session_change_task, client):
    response = await client.put(
        '/tasks/',
        json={'id': 1, 'title': 't2', 'description': 'd2'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['title'] == 't2'
    assert data['description'] == 'd2'


@pytest.fixture()
def override_db_session_delete_task():
    async def override_get_async_session():
        class FakeSession:
            async def get(self, model, id_):
                return Task(id=id_, title='t1', description='d1', completed=False, created_at=datetime.now())

            async def delete(self, obj):
                pass

            async def commit(self):
                pass

        yield FakeSession()

    app.dependency_overrides[get_async_session] = override_get_async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)


@pytest.mark.anyio
async def test_delete_task(override_db_session_delete_task, client):
    response = await client.delete('/tasks/', params={'task_id': 1})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1


@pytest.fixture()
def override_db_session_complete_task():
    async def override_get_async_session():
        class FakeSession:
            async def get(self, model, id_):
                return Task(id=id_, title='t1', description='d1', completed=False, created_at=datetime.now())

            async def commit(self):
                pass

        yield FakeSession()

    app.dependency_overrides[get_async_session] = override_get_async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)


@pytest.mark.anyio
async def test_complete_task(override_db_session_complete_task, client):
    response = await client.patch('/tasks/', params={'task_id': 1, 'checked': True})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['checked'] is True
