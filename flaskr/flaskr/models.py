import peewee
from flask import current_app
from os import path

db_path = path.join(current_app.instance_path, 'flaskr.sqlite')

db = peewee.SqliteDatabase(db_path)


class BaseModel(peewee.Model):
    class Meta:
        database = db
        db_file = db_path


class User(BaseModel):
    id = peewee.AutoField(primary_key=True)
    username = peewee.CharField(unique=True, null=False)
    password = peewee.CharField(null=False)


# Define a model for the "room" table
class Room(BaseModel):
    id = peewee.ForeignKeyField(User, backref='rooms', column_name='id')
    name = peewee.CharField(unique=True, null=False)
    password = peewee.CharField(null=False)
    creator = peewee.ForeignKeyField(User, backref='rooms', column_name='creator')
    created = peewee.TimestampField(null=False, default=peewee.datetime.datetime.now)


# Define a model for the "game" table
class Game(BaseModel):
    id = peewee.ForeignKeyField(User, backref='games', column_name='id')
    player_id = peewee.ForeignKeyField(User, backref='games', column_name='player_id', unique=True, null=False)


# Define a model for the "open_stats" table
class OpenStat(BaseModel):
    room_id = peewee.ForeignKeyField(Room, backref='open_stats', column_name='room_id')
    player_id = peewee.ForeignKeyField(User, backref='open_stats', column_name='player_id', null=False)
    profession = peewee.BooleanField()
    biology = peewee.BooleanField()
    health = peewee.BooleanField()
    hobby = peewee.BooleanField()
    baggage = peewee.BooleanField()
    facts = peewee.BooleanField()
    special_cards = peewee.BooleanField()
    disaster = peewee.BooleanField()
