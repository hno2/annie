from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_dropzone import Dropzone


db = SQLAlchemy()


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


dropzone = Dropzone()
