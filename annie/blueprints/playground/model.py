from annie.extensions import BaseMixin, db
from annie.blueprints.user.model import Submission, UserModel
from sqlalchemy.ext.associationproxy import association_proxy

showcase_tags = db.Table(
    "showcasetags",
    db.Column(
        "showcase_id", db.Integer, db.ForeignKey("showcases.id"), primary_key=True
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

showcase_votes = db.Table(
    "showcasevotes",
    db.Column(
        "showcase_id", db.Integer, db.ForeignKey("showcases.id"), primary_key=True
    ),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


def _tag_find_or_create(tag_name: str):
    """Creates tag if it doesn't exist

    Returns:
        [Tag]: The tag object
    """
    tag = Tag.query.filter_by(name=tag_name).first()
    if not (tag):
        tag = Tag(name=tag_name)

    return tag


class Showcase(BaseMixin, db.Model):
    __tablename__ = "showcases"
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    submission = db.relationship(
        Submission,
        backref=db.backref("showcase", uselist=False),
        lazy=True,
        uselist=False,
    )
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"))
    tg = db.relationship("Tag", secondary=lambda: showcase_tags, backref="showcases")
    tags = association_proxy(  # Proxy the name of the tg relationship
        "tg", "name", creator=_tag_find_or_create
    )
    # Relationship between UserModel and Showcase
    voted_users = db.relationship(
        "UserModel", secondary=lambda: showcase_votes, backref="voted_showcases"
    )

    @classmethod
    def upvote(cls, showcase_id: int, token: str):
        # Check that user has not already upvoted
        user = UserModel.get_by_token(token)
        if not user:
            print("No user")
            return False
        showcase = Showcase.query.get(showcase_id)
        if user not in showcase.voted_users:
            showcase.voted_users.append(user)
            showcase.score = len(showcase.voted_users)
            showcase.save()
        return showcase

    @classmethod
    def getrecent(cls, limit: int = 20):
        return Showcase.query.order_by(Showcase.id.desc()).limit(limit).all()

    @classmethod
    def getpopular(cls, limit: int = 20):
        return Showcase.query.order_by(Showcase.score.desc()).limit(limit).all()

    @classmethod
    def get_by_tag(cls, tag, limit: int = 20):
        return (
            Showcase.query.join(Showcase.tg)
            .filter(Tag.name == tag)
            .order_by(Showcase.score.desc())
            .limit(limit)
            .all()
        )

    def __repr__(self):
        return "<Showcase {name} - Submission {submission} - score {score}>".format(
            name=self.name,
            score=self.score,
            submission=self.submission,
        )


class Tag(BaseMixin, db.Model):
    __tablename__ = "tags"
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Tag %r>" % self.name

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_limit(cls, limit: int = 100):
        return Tag.query.limit(limit).all()
