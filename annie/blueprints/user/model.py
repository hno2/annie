from annie.extensions import db, BaseMixin
import shortuuid
from annie.blueprints.evaluation.model import Grade


class UserModel(BaseMixin, db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(80), unique=True, nullable=False)
    auth_token = db.Column(db.String(40), unique=True, default=shortuuid.uuid)
    submissions = db.relationship(
        "Submission",
        backref=db.backref("user", lazy=True),
        order_by="Submission.created.desc()",
    )

    def __repr__(self):
        return "<User %r>" % self.username

    @classmethod
    def get_by_username(cls, username):
        return UserModel.query.filter(UserModel.username == username).first()

    @classmethod
    def get_by_token(cls, token):
        return UserModel.query.filter(UserModel.auth_token == token).first()

    @classmethod
    def get_by_id(cls, id):
        return UserModel.query.get(id)


assigned = db.Table(
    "assigned",
    db.Column("assignment", db.Integer, db.ForeignKey("assignments.id")),
    db.Column("user", db.Integer, db.ForeignKey("users.id")),
)


class Assignment(BaseMixin, db.Model):
    __tablename__ = "assignments"
    title = db.Column(db.String(40), nullable=False)
    github = db.Column(db.String(40))
    description = db.Column(db.String(80))
    users = db.relationship(
        "UserModel",
        secondary=assigned,
        backref=db.backref("assignments", lazy=True),
    )
    path = db.Column(db.Unicode(128), default=None)  # None if not static check
    max_submissions = db.Column(db.Integer, default=100)

    def __repr__(self):
        return "<Assignment %r>" % self.title

    @classmethod
    def get_by_id(cls, id):
        return Assignment.query.filter(Assignment.id == id).first()

    @classmethod
    def get_by_name(cls, name):
        return Assignment.query.filter(Assignment.title == name).first()


class Submission(BaseMixin, db.Model):
    __tablename__ = "submissions"
    filepath = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"))
    assignment = db.relationship(
        Assignment,
        backref=db.backref("submissions", order_by="Submission.created.desc()"),
    )

    grade = db.relationship(Grade, backref="submission", uselist=False)

    def __repr__(self):
        return "<Submission by {} for Assignment {}>".format(self.user, self.assignment)

    @classmethod
    def get_by_id(cls, id):
        return Submission.query.get(id)
