# This file should contain records you want created when you run flask db seed.
from annie.blueprints.user.model import User, Assignment, Submission


itw = Assignment(
    static=False,
    title="Into the wild",
    github="/fastai/fastai/blob/master/nbs/examples/ulmfit.ipynb",
)
pd = Assignment(
    static=True,
    title="Getting Started with Pandas",
    github="fastai/fastai/blob/master/nbs/examples/camvid.ipynb",
)

test_user = {
    "username": "Simon Klug",
    "assignments": [itw, pd],
    "submissions": [
        Submission(assignment=itw),
        Submission(assignment=itw),
        Submission(assignment=pd),
    ],
}

User(**test_user).save()
