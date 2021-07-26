# This file should contain records you want created when you run flask db seed.
from annie.blueprints.user.model import Grade, UserModel, Assignment, Submission


itw = Assignment(
    static=False,
    title="Into the wild",
    github="/hno2/annie/blob/main/example.ipynb",
)
pd = Assignment(
    static=True,
    title="Pandas retten den Tag",
    description="Hier lernt man wie man mit Daten umgeht und was Pandas so ist",
    github="/hno2/annie/blob/main/example.ipynb",
    max_submissions=1,
)
itw.save()
pd.save()
gradeone = Grade(static=90, ai=80, overall=70, peer=100)
gradetwo = Grade(static=60, ai=90, overall=30, peer=10)
gradethree = Grade(static=10, ai=60, overall=100, peer=80)

test_user = {"username": "Dummy User", "assignments": [itw, pd]}
user = UserModel(**test_user).save()
