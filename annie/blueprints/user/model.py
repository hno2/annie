from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)


class UserModel(TimestampMixin, db.Model):
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
        return UserModel.query.filter(UserModel.username == username).first()

    @classmethod
    def find_by_id(cls, id):
        return UserModel.query.filter(UserModel.id == id).first()

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

    @classmethod
    def find_by_id(cls, id):
        return Assignment.query.filter(Assignment.id == id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    static = db.Column(db.Integer)
    ai = db.Column(db.Integer)
    peer = db.Column(db.Integer)
    overall = db.Column(
        db.Integer
    )  # Maybe we should add the content of peer Review here.
    submission_id = db.Column(
        db.Integer, db.ForeignKey("submissions.id"), nullable=False
    )

    def __repr__(self):
        return "<Grade {overall} (AI-{ai}/Static-{static}/Peer-{peer}) for Submission {submission}>".format(
            overall=self.overall,
            ai=self.ai,
            static=self.static,
            peer=self.peer,
            submission=self.submission,
        )


class Submission(TimestampMixin, db.Model):
    __tablename__ = "submissions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"))
    user = db.relationship(
        UserModel,
        backref=db.backref("submissions", order_by="Submission.created.desc()"),
    )
    assignment = db.relationship(Assignment, backref=db.backref("submissions"))
    grade = db.relationship(Grade, backref="submission", uselist=False)

    def __repr__(self):
        return "<Submission by {} for Assignment {}>".format(self.user, self.assignment)
