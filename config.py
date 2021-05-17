import os

try:
    HASH = os.environ["GIT_COMMIT"]
except:
    HASH = "not available"

DEBUG = True


PYLTI_CONFIG = {
    "consumers": {
        "ki-campus": {"secret": os.environ.get("CONSUMER_KEY_SECRET", "secret")}
    }
}
