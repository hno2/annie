import os

try:
    HASH = os.environ["GIT_COMMIT"]
except:
    HASH = "not available"

DEBUG = True
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(16))

PYLTI_CONFIG = {
    "consumers": {
        "ki-campus": {"secret": os.environ.get("CONSUMER_KEY_SECRET", "secret")}
    }
}
## UPLOAD STUFF
UPLOAD_FOLDER = "uploads"  # Submissions and Assignment files will be added here, make sure this folder exists
ALLOWED_EXTENSIONS = {"ipynb", "txt", "py"}
DROPZONE_ALLOWED_FILE_CUSTOM = True
DROPZONE_ALLOWED_FILE_TYPE = ".ipynb, .py, .txt"

SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Celery Broker Things
BROKER_URL = os.getenv("REDIS_URL", "pyamqp://guest@localhost//")


# Celery.
CELERY_CONFIG = {
    "broker": BROKER_URL,
    "include": ["annie.blueprints.evaluation.tasks"],
}
ENABLE_SHOWCASE = True
ENABLE_CLIPPY = True
ENABLE_GRADER = True
