from threading import main_thread
from flask_sqlalchemy import SQLAlchemy
import os

try:
    os.remove("test.db")
except:
    pass
db = SQLAlchemy()


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.username
        
    @classmethod
    def find_by_username(cls, id):
        return User.query.filter(User.id == id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(60), nullable=False)
    status = db.Column(db.Integer, nullable=False)  # 0 for in progress 1 done
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignment = db.relationship("Assignment", backref="task", lazy=True)
    assignment_id = db.Column(
        db.Integer, db.ForeignKey("assignment.id"), nullable=False
    )
    assignment = db.relationship("Assignment", backref=db.backref("tasks", lazy=True))

    def __repr__(self):
        return "<Task %r>" % self.file


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    static = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return "<Assignment %r>" % self.file


if __name__ == "__main__":
    db.create_all()
    itw = Assignment(static=False, name="Into the wild")
    pd = Assignment(static=True, name="Getting Started with Pandas")
    first = Task(
        file="uploads/5_KI_einfach_machen_Roboter_Muster.ipynb",
        status="0",
        assignment=itw,
    )
    second = Task(
        file="uploads/1_python_uebung_Muster2.ipynb", status="1", assignment=pd
    )
    simon = User(username="simon", lti_id=0)

    simon.tasks.extend([first, second])

    db.session.add(simon)
    db.session.add_all([first, second])

    db.session.commit()
