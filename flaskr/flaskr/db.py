import click
from flask import current_app, g
from peewee import SqliteDatabase
from flaskr.models import User, Room, Game, OpenStat


def get_db():
    if 'db' not in g:
        g.db = SqliteDatabase(current_app.config['DATABASE'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    with current_app.app_context():
        db = get_db()
        with db:
            db.drop_tables((User, Room, Game, OpenStat), safe=True, on_delete='CASCADE')
            db.create_tables((User, Room, Game, OpenStat))


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialised the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
