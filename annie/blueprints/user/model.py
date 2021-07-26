from annie.extensions import db, TimestampMixin
import shortuuid


class UserModel(TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    auth_token = db.Column(db.String(40), unique=True, default=shortuuid.uuid())
    submissions = db.relationship(
        "Submission",
        backref=db.backref("user", lazy=True),
        order_by="Submission.created.desc()",
    )

    def __repr__(self):
        return "<User %r>" % self.username

    @classmethod
    def find_by_username(cls, username):
        return UserModel.query.filter(UserModel.username == username).first()

    @classmethod
    def find_by_token(cls, token):
        return UserModel.query.filter(UserModel.auth_token == token).first()

    @classmethod
    def find_by_id(cls, id):
        return UserModel.query.filter(UserModel.id == id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


assigned = db.Table(
    "assigned",
    db.Column("assignment", db.Integer, db.ForeignKey("assignments.id")),
    db.Column("user", db.Integer, db.ForeignKey("users.id")),
)


class Assignment(TimestampMixin, db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    static = db.Column(db.Boolean, nullable=False)
    github = db.Column(db.String(40))
    description = db.Column(db.String(80))
    users = db.relationship(
        "UserModel",
        secondary=assigned,
        backref=db.backref("assignments", lazy=True),
    )
    path = db.Column(db.Unicode(128))
    max_submissions = db.Column(db.Integer, default=100)

    def __repr__(self):
        return "<Assignment %r>" % self.title

    @classmethod
    def find_by_id(cls, id):
        return Assignment.query.filter(Assignment.id == id).first()

    @classmethod
    def find_by_name(cls, name):
        return Assignment.query.filter(Assignment.title == name).first()

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
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"))

    def __repr__(self):
        return "<Grade {overall} (AI-{ai}/Static-{static}/Peer-{peer}) for Submission {submission}>".format(
            overall=self.overall,
            ai=self.ai,
            static=self.static,
            peer=self.peer,
            submission=self.submission,
        )


class Showcase(TimestampMixin, db.Model):
    __tablename__ = "showcases"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Maybe instead of a number score, the score will be user_ids of the users who upvoted. Score is then calculated by the number of users who upvoted.
    score = db.Column(db.Integer, nullable=False, default=0)
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"))

    @classmethod
    def upvote(cls, showcase_id):
        showcase = Showcase.query.filter(Showcase.id == showcase_id).first()

        showcase.score += 1
        showcase.save()
        return showcase

    @classmethod
    def getrecent(cls, limit: int = 20):
        return Showcase.query.order_by(Showcase.id.desc()).limit(limit).all()

    @classmethod
    def getpopular(cls, limit: int = 20):
        return Showcase.query.order_by(Showcase.score.desc()).limit(limit).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return "<Showcase {name} - Submission {submission} - score {score}>".format(
            name=self.name,
            score=self.score,
            submission=self.submission,
        )


class Submission(TimestampMixin, db.Model):
    __tablename__ = "submissions"
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"))
    assignment = db.relationship(
        Assignment,
        backref=db.backref("submissions", order_by="Submission.created.desc()"),
    )
    showcase = db.relationship(
        Showcase, backref=db.backref("submission", uselist=False)
    )
    grade = db.relationship(Grade, backref="submission", uselist=False)

    def __repr__(self):
        return "<Submission by {} for Assignment {}>".format(self.user, self.assignment)
