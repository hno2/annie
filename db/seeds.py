# This file should contain records you want created when you run flask db seed.
from annie.blueprints.user.model import Grade, UserModel, Assignment, Submission


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
gradeone = Grade(static=90, ai=80, overall=70, peer=100)
gradetwo = Grade(static=60, ai=90, overall=30, peer=10)
gradethree = Grade(static=10, ai=60, overall=100, peer=80)

test_user = {
    "username": "Simon Klug",
    "submissions": [
        Submission(assignment=itw, grade=gradeone),
        Submission(assignment=itw, grade=gradetwo),
        Submission(assignment=pd, grade=gradethree),
    ],
}
user = UserModel(**test_user).save()
pd.users.append(user)
itw.users.append(user)
itw.save()
pd.save()
