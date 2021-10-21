from annie.extensions import db, BaseMixin
import shortuuid
from flask import current_app
from annie.blueprints.evaluation.model import Grade
import os
from sqlalchemy.event import listens_for


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
    def get_by_token_or_404(cls, token):
        return UserModel.query.filter(UserModel.auth_token == token).first_or_404(
            description="User not found"
        )

    @classmethod
    def get_by_token(cls, token):
        return UserModel.query.filter(UserModel.auth_token == token).first()

    @classmethod
    def get_by_id(cls, id):
        return UserModel.query.get(id)

    def get_submissions_by_assignment(user, assignment):
        return (
            Submission.query.filter(Submission.user_id == user.id)
            .filter(Submission.assignment_id == assignment.id)
            .order_by(Submission.created.desc())
            .all()
        )


assigned = db.Table(
    "assigned",
    db.Column("assignment", db.Integer, db.ForeignKey("assignments.id")),
    db.Column("user", db.Integer, db.ForeignKey("users.id")),
)


class Assignment(BaseMixin, db.Model):
    __tablename__ = "assignments"
    title = db.Column(db.String(40), nullable=False)
    github = db.Column(db.String(40), default=None)
    description = db.Column(db.String(80))
    due_date = db.Column(db.DateTime)
    users = db.relationship(
        "UserModel",
        secondary=assigned,
        backref=db.backref("assignments", lazy=True),
    )
    autograder_path = db.Column(
        db.Unicode(128), default=None
    )  # None if not static check
    showcaseable = db.Column(db.Boolean, default=False)
    student_nb = db.Column(db.Unicode(128), default=None)
    master_nb = db.Column(db.Unicode(128), default=None)  # None if not static check
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

    @classmethod
    def get_by_filepath(cls, path):
        return Submission.query.filter(Submission.filepath == path).first()

    @classmethod
    # Get all submission without a grade
    def get_all_without_grade(cls):
        return Submission.query.filter((Submission.grade == None)).count()


# Delete hooks for models, delete files if models are getting deleted
@listens_for(Submission, "after_delete")
def del_file(mapper, connection, target):
    if target.filepath:
        try:
            os.remove(
                os.path.join(
                    os.getcwd(),
                    current_app.config["UPLOAD_FOLDER"],
                    "submissions",
                    target.filepath,
                )
            )
        except OSError:
            pass
