import os

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(logger=True, engineio_logger=True)

def create_app(test_config=None, debug=False):
    app = Flask(__name__, instance_relative_config=True)
    app.debug = debug
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    with app.app_context():
        from . import db
        from . import auth
        from . import index
        from . import game

        from . import middleware

        db.init_app(app)

        app.register_blueprint(auth.bp)
        app.register_blueprint(index.bp)
        app.register_blueprint(game.bp)

        app.after_request(middleware.add_location_header)

        socketio.init_app(app)

    return app
