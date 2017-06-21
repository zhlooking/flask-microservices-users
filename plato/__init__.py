import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS


# instantiate the db
db = SQLAlchemy()


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # 解决跨域请求的问题
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # setup extensions
    db.init_app(app)

    # register blueprints
    from plato.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app
