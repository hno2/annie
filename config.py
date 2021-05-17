import os

try:
    HASH = os.environ["GIT_COMMIT"]
except:
    HASH = "not available"

DEBUG = True
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "random-key")

PYLTI_CONFIG = {
    "consumers": {
        "ki-campus": {"secret": os.environ.get("CONSUMER_KEY_SECRET", "secret")}
    }
}
