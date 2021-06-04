from flask import Flask
from celery import Celery
from annie.blueprints.eval import eval
from annie.blueprints.user import user
from flask_dropzone import Dropzone


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
    from annie.blueprints.user.model import db

    db.init_app(app)
    # Maybe Move this first line to the corresponding blueprint
    dropzone = Dropzone()
    dropzone.init_app(app)
    app.register_blueprint(eval)
    app.register_blueprint(user)

    return app


celery_app = create_celery_app()
