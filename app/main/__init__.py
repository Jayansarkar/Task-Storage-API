from flask import Flask

from werkzeug.contrib.fixers import ProxyFix
from flask_bcrypt import Bcrypt

from app.main.config import config_by_name
from app.main.db import init_app as db_init

flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    flask_bcrypt.init_app(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    db_init(app)

    return app
