from flaskr import create_app
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
        