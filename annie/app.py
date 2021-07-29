from flask import Flask
from celery import Celery
from annie.blueprints.evaluation import evaluation
from annie.blueprints.user import user
from annie.blueprints.showcase import showcase

from annie.extensions import db, dropzone

import os


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.
    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name)
    celery.conf.update(app.config.get("CELERY_CONFIG", {}))
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.
    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, static_folder="../static", static_url_path="")

    app.config.from_object("config.settings")

    if settings_override:
        app.config.update(settings_override)

    os.makedirs(app.config["UPLOAD_FOLDER"] + "/submissions/", exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"] + "/assignments/master", exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"] + "/assignments/student", exist_ok=True)

    db.init_app(app)
    dropzone.init_app(app)
    with app.app_context():
        from annie.blueprints.admin.model import admin

    admin.init_app(app)

    app.register_blueprint(evaluation)
    app.register_blueprint(user)
    if app.config["ENABLE_SHOWCASE"]:
        app.register_blueprint(showcase)

    return app


celery_app = create_celery_app()
