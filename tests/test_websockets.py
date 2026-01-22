from fastapi.testclient import TestClient
from main import app


def test_websocket():
    client1 = TestClient(app)
    client2 = TestClient(app)
    
    with client1.websocket_connect('/ws/table/?username=n') as connect1,\
        client2.websocket_connect('/ws/table/?username=type') as connect2:

        data = {'username': 'n', 'pass': '123'}
        connect1.send_json(data)

        assert connect1.receive_json() == data
        assert connect2.receive_json() == data
