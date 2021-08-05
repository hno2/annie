from annie.extensions import db, BaseMixin


class Grade(BaseMixin, db.Model):
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
