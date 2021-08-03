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
    description="Bei Into the Wild, darfst du deine eigene Fragestellung bearbeiten. Ob die Analyse von Tweets, Sprach- oder Texterkennung oder Bilderkennung, was kannst du in vier Wochen schaffen?",
    github="/hno2/example_assignment/blob/main/example.ipynb",
)
pd = Assignment(
    title="Pandas retten den Tag",
    description="Pandas sind tolle Tiere und die Standart Python Bibliothek für Tabellendaten.",
    github="/hno2/example_assignment/blob/main/example.ipynb",
    path="autograder.zip",
)
itw.save()
pd.save()
gradeone = Grade(static=90, overall=90)
gradetwo = Grade(static=60, overall=60)
gradethree = Grade(static=10, overall=10)

subone = Submission(assignment=pd, grade=gradeone, filepath="./example.ipynb")
subtwo = Submission(assignment=pd, grade=gradetwo, filepath="./example.ipynb")
subthree = Submission(assignment=pd, grade=gradethree, filepath="./example.ipynb")

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


test_user = {
    "username": "Dummy User",
    "assignments": [itw, pd],
    "submissions": [subone, subtwo, subthree],
}
user = UserModel(**test_user).save()
