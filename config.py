import os

try:
    HASH = os.environ["GIT_COMMIT"]
except:
    HASH = "not available"

DEBUG = True
