from flask import Blueprint, render_template, request
from annie.blueprints.showcase.model import Showcase

showcase = Blueprint("showcase", __name__, template_folder="templates")


@showcase.route("/showcase")
def overview():

    return render_template("showcase.html", showcases=Showcase)


@showcase.route("/upvote", methods=["POST"])
def upvote():
    # TODO: Each User can only upvote once per Showcase
    try:
        Showcase.upvote(request.form["showcase_id"])
        return "OK", 200
    except Exception as e:
        return "Error: " + str(e), 500


@showcase.route("/add_showcase", methods=["POST"])
def add_showcase():
    Showcase(
        name=request.form["title"],
        description=request.form["description"],
    ).save()
    # tags = request.form["tags"]
    return "OK", 200
