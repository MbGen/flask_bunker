from flask import Blueprint, request, render_template, flash, redirect, url_for, session, g
from flask_socketio import join_room, leave_room, send, emit

from flaskr.db import get_db
from .auth import login_required
from . import socketio

bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/lobby/<int:lobby_id>', methods=('GET', 'POST'))
@login_required
def lobby(lobby_id: int):
    db = get_db()
    error = None
    if not is_exists_lobby(lobby_id):
        error = 'The lobby doesn\'t exists'
        flash(error)
        return redirect(url_for('index.index'))

    if request.referrer is None:
        error = "You are not registered in this lobby"
        flash(error)
        return redirect(url_for('index.index'))

    players = db.execute("""
    SELECT g.id, g.player_id, u.username FROM game as g
    INNER JOIN user as u ON g.player_id=u.id
    WHERE g.id = ?""", (lobby_id, )).fetchall()

    return render_template("game/lobby.html", lobby_id=lobby_id, players=players, player=g.user)

def is_exists_lobby(lobby_id: int) -> bool:
    db = get_db()
    return db.execute("SELECT id FROM room WHERE id=?", (lobby_id, )).fetchone() is not None


def get_list_of_players_id(lobby_id: int) -> list:
    db = get_db()
    rows = db.execute("SELECT player_id FROM game WHERE id=?", (lobby_id, )).fetchall()
    return [row['player_id'] for row in rows]


@socketio.on('join')
def on_join(data):
    db = get_db()
    user_id = data['user_id'] 
    username = data['username']
    room = data['room_id']

    user_data = {
        'userId': user_id,
        'username': username,
        'method': 'join'
    }

    if int(user_id) not in get_list_of_players_id(room):
        with db:
            db.execute("INSERT INTO game (id, player_id) VALUES (?, ?)", (room, user_id))
        join_room(room)
        send(user_data, json=True, room=room)


@socketio.on('leave')
def on_leave(data):
    db = get_db()
    user_id = data['user_id']
    username = data['username']
    room = data['room_id']

    player_info = {
        'userId': user_id,
        'username': username,
        'method': 'leave'
    }

    with db:
        db.execute("DELETE FROM game WHERE player_id=?", (user_id, ))
        send(player_info, json=True, room=room)
        leave_room(room)
