from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_dropzone import Dropzone


db = SQLAlchemy()


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)


dropzone = Dropzone()
