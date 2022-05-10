import datetime
import logging
import os
from pathlib import Path

from flask import Flask
from flask.logging import default_handler


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # logger
    app.logger.removeHandler(default_handler)
    log_folder = Path(app.instance_path) / f'log'
    os.makedirs(log_folder, exist_ok=True)
    log_handler = logging.FileHandler(log_folder / f'system.{datetime.date.today().strftime("%Y%m")}.log')
    log_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.DEBUG)

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
    account.init_login_manager(app)
    app.register_blueprint(account.router)
    app.register_blueprint(index.router)
    maintenance_url.register_url(app)

    from terminator.maintenance.biz import reload_schedule
    reload_schedule(app)

    return app
