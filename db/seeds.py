from datetime import datetime, timedelta

# This file should contain records you want created when you run flask db seed.
from annie.blueprints.user.model import (
    UserModel,
    Assignment,
    Submission,
)
from annie.blueprints.evaluation.model import Grade
from annie.blueprints.playground.model import Showcase, Tag
from annie.blueprints.clippy.model import Chat, Message


itw = Assignment(
    title="Into the wild",
    description="You are on your own now! In the Into the Wild, you get to work on your own question. Whether it's analyzing tweets, recognizing speech or working with images, show us what can you accomplish in four weeks!",
    github="/hno2/example_assignment/blob/main/example.ipynb",
    due_date=datetime.today() + timedelta(days=21),
    showcaseable=True,
)
pd = Assignment(
    title="Pandas save the Day",
    description="In this assignment we will deal with data and different data types. The focus is on the best known form, the CSV format, whose properties and special features will be examined in detail.  Afterwards we will show you how to import data with the help of the Pandas Library. This simplifies the import of data enormously - so Pandas save the day. ",
    github="/hno2/example_assignment/blob/main/example.ipynb",
    master_nb="Task 1 - Data Preparation.ipynb",
    student_nb="Task 1 - Data Preparation_Empty.ipynb",
    due_date=datetime.today() + timedelta(days=14),
)
itw.save()
pd.save()
gradeone = Grade(static=90)
gradetwo = Grade(static=60)
gradethree = Grade(static=10)

subone = Submission(assignment=pd, grade=gradeone, filepath="example.ipynb")
subtwo = Submission(assignment=pd, grade=gradetwo, filepath="example2.ipynb")
subthree = Submission(assignment=pd, grade=gradethree, filepath="example3.ipynb")

Showcase(
    name="Classification of covid lung images",
    description="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    submission=subone,
    score=10,
    tags=["classification", "medical", "covid"],
).save()
Showcase(
    name="Time Series Prediction of future sales",
    description="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    submission=subtwo,
    score=2,
    tags=["regression", "finance", "time series"],
).save()
Showcase(
    name="Clustering of Tweets from Donald Trump",
    description="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
    submission=subthree,
    score=0,
    tags=["clustering", "transformers", "nlp"],
).save()

subnograde = Submission(assignment=pd, filepath="4hnzKz7YFqmkMjv8kgRkxe.ipynb").save()

test_user = {
    "username": "Dummy User",
    "assignments": [itw, pd],
    "submissions": [subnograde],
}
user = UserModel(**test_user).save()

simon = {
    "username": "Simon",
    "assignments": [itw, pd],
    "submissions": [subone, subtwo, subthree],
}
simon = UserModel(**simon).save()
