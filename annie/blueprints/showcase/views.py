from flask import Blueprint, render_template, request
from annie.blueprints.user.model import Showcase

showcase = Blueprint("showcase", __name__, template_folder="templates")


@showcase.route("/showcase")
def overview():

    return render_template("showcase.html", showcases=Showcase)


@showcase.route("/upvote", methods=["POST"])
def upvote():
    # TODO: Each User can only upvote once per Showcase
    print(request.form["showcase_id"])
    Showcase.upvote(request.form["showcase_id"])
    return "OK", 200
