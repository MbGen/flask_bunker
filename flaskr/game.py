from flask import Blueprint, request, render_template, flash, redirect, url_for, session, g
from flask_socketio import join_room, leave_room, send, emit

from flaskr.db import get_db
from . import socketio

bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/lobby/<int:lobby_id>', methods=('GET', 'POST'))
def lobby(lobby_id: int):
    db = get_db()
    error = None
    if not is_exists_lobby(lobby_id):
        error = 'The lobby doesn\'t exists'
        flash(error)
        return redirect(url_for('index.index'))

    if not session.get('user_id') in get_list_of_players_id(lobby_id):
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
    username = data['username']
    room = data['room_id']
    user_id = data['user_id'] 
    if int(user_id) in get_list_of_players_id(room):
        return
    json = {
        'userId': user_id,
        'username': username,
    }
    join_room(room)
    send(json, json=True, to=room)
    # send(username + " Has join the room", to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room_id']
    leave_room(room)
    send(username + " Has left the room", to=room)