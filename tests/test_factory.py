from flaskr import create_app, db
from conftest import AuthActions
from flask.testing import FlaskClient


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_unlogged_index(client: FlaskClient):
    """
    Test when user is unlogged for root '/'
    """
    response = client.get('/')
    assert b'Log in' in response.data 


def test_logged_index(client: FlaskClient, auth: AuthActions):
    """
    Test when user is logged in for root '/'
    """
    auth.login()
    response = client.get('/')

    assert b'Create Lobby' in response.data
    assert b'Find Game' in response.data
    assert b'Log Out' in response.data

# TODO: refactor
def test_create_lobby(client: FlaskClient, auth: AuthActions, app):
    response = client.get('/') 
    assert 302 >= response.status_code >= 200 
    assert response.location == 'http://localhost/'

    auth.login()

    lobby_info = {
            "lobbyname": "alo",
            "lobbypassword": "123",
            "action": "create_lobby"}

    headers = {'Content-Type': 'multipart/form-data'}

    response = client.post(
        '/',
        data=lobby_info,
        headers=headers)

    with app.context():
        _db = db.get_db()
        assert len(_db.execute('SELECT * FROM room WHERE id=?').fetchall()) == 1

    assert 302 >= response.status_code >= 200 
    assert response.location == '/game/lobby/1'

# TODO: refactor
def test_connect(client: FlaskClient, auth: AuthActions):
    response = client.get('/') 
    assert response.status_code == 200
    auth.login()
    lobby_create = {
        'lobbyname': 'alo',
        'lobbypassword': '123',
        'action': 'create_lobby'
    } 
    lobby_join = {
        'lobbyname': 'alo',
        'lobbypassword': '123',
        'action': 'join_lobby'
    }
    headers = {'Content-Type': 'multipart/form-data'}

    response = client.post(
        '/',
        data=lobby_create,
        headers=headers
    )

    auth.logout()
    auth.login('other', 'other')

    response = client.post(
        '/',
        data=lobby_join,
        headers=headers
    )

    assert response.status_code == 200
    assert response.location == '/game/lobby/'




