from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    assignments = db.relationship(
        "Assignment",
        secondary="submissions",
        backref=db.backref("users", lazy=True, viewonly=True),
        viewonly=True,
    )

    def __repr__(self):
        return "<User %r>" % self.username

    @classmethod
    def find_by_username(cls, username):
        return User.query.filter(User.username == username).first()

    @classmethod
    def find_by_id(cls, id):
        return User.query.filter(User.id == id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Assignment(TimestampMixin, db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    static = db.Column(db.Boolean, nullable=False)
    github = db.Column(db.String(40))

    def __repr__(self):
        return "<Assignment %r>" % self.title

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self


class Submission(TimestampMixin, db.Model):
    __tablename__ = "submissions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"))
    user = db.relationship(User, backref=db.backref("submissions"))
    assignment = db.relationship(
        Assignment,
        backref=db.backref("submissions"),
    )

    def __repr__(self):
        return "<Submission by {} for Assignment {}>".format(self.user, self.assignment)
