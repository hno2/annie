from annie.extensions import db, BaseMixin
from sqlalchemy.event import listens_for
from statistics import mean
import bleach
from markdown import markdown


class Grade(BaseMixin, db.Model):
    static = db.Column(db.Integer)
    manual = db.Column(db.Integer, default=None)
    ai = db.Column(db.Integer)
    peer = db.Column(db.Integer)
    overall = db.Column(
        db.Integer
    )  # Maybe we should add the content of peer Review here.
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"))
    manual_description = db.Column(db.String(255))

    def __repr__(self):
        return "<Grade {overall} (AI-{ai}/Static-{static}/Peer-{peer}/Manual-{manual}) for Submission {submission}>".format(
            overall=self.overall,
            ai=self.ai,
            static=self.static,
            peer=self.peer,
            submission=self.submission,
            manual=self.manual,
        )


@listens_for(Grade, "before_insert")
def _update_overall(mapper, connection, target):
    # Update Overall Grader
    all_grades = []
    for grade in [target.ai, target.static, target.peer, target.manual]:
        if grade is not None:
            all_grades.append(grade)
    target.overall = int(mean(all_grades))


class Comment(BaseMixin, db.Model):
    markdown = db.Column(db.String(500))
    html = db.Column(db.String(500))
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"))
    user = db.relationship("UserModel", backref="comments")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    cell_id = db.Column(db.String(80))

    def __repr__(self):
        return "<Comment {markdown}>".format(
            markdown=self.markdown,
        )


def strip(s: str):
    """strips outer html tags"""

    start = s.find(">") + 1
    end = len(s) - s[::-1].find("<") - 1

    return s[start:end]


@listens_for(Comment, "before_insert")
def _update_html(mapper, connection, target):
    # Updates the html fields with the markdown
    target.html = bleach.clean(  # Sanitize the comment with bleach
        strip(  # Markdown introduces extra html tags we need to strip
            markdown(
                target.markdown,
            )
        )
    )
