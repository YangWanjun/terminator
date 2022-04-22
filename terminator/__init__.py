import os

from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # load default config
    app.config.from_object('terminator.config')
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    from . import database
    database.init_app(app)

    from . import account, index
    from .maintenance import urls as maintenance_url
    app.register_blueprint(account.router)
    app.register_blueprint(index.router)
    maintenance_url.register_url(app)

    from .hooks import register_hooks
    register_hooks(app)

    from terminator.maintenance.biz import reload_schedule
    reload_schedule(app)

    return app
