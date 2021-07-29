from annie.extensions import db, TimestampMixin
from annie.blueprints.user.model import Submission


class Showcase(TimestampMixin, db.Model):
    __tablename__ = "showcases"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Maybe instead of a number score, the score will be user_ids of the users who upvoted. Score is then calculated by the number of users who upvoted. Or in User Model ids of upvoted
    score = db.Column(db.Integer, nullable=False, default=0)
    submission = db.relationship(
        Submission, backref="showcase", lazy=True, uselist=False
    )
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"))
    #    tags=db.relationship('Tag', secondary='showcase_tags', backref='showcases')
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


class Tag(TimestampMixin, db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Tag %r>" % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_limit(cls, limit: int = 100):
        return Tag.query.limit(limit).all()
