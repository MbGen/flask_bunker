from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    match request.method:
        case 'POST':
            lobby_name = request.form['lobbyname']
            lobby_password = request.form['lobbypassword']
            action = request.form['action']
            user_id = session.get('user_id')

            match action:
                case 'create_lobby':
                    # TODO: провiряти чи вже не створенно лобi з таким id, я добавив свойство UNIQUE до id, то мона провiряти черех try except Integrity error вродi
                    return create_lobby(lobby_name, lobby_password, user_id) 
                case 'join_lobby':
                    return join_lobby(lobby_name, lobby_password, user_id)

    return render_template('index.html')


def create_lobby(name, password, creator_id):
    db = get_db()
    try:
        with db:
            db.execute(
                "INSERT INTO room (id, name, password, creator) VALUES (?, ?, ?, ?)", (
                    creator_id, name, generate_password_hash(password), creator_id)
            )
    except db.IntegrityError:
        error = "Lobby with this name is already exists"
        flash(error)

    return redirect(url_for('game.lobby', lobby_id=creator_id))


def join_lobby(lobby_name, lobby_password, user_id):
    db = get_db()
    lobby = db.execute("SELECT id, name, password FROM room WHERE name=?", (lobby_name, )).fetchone()
    if check_password_hash(lobby['password'], lobby_password):
        return redirect(url_for('game.lobby', lobby_id=lobby['id']))

    error = 'Incorrect lobby password'
    flash(error)