from annie.blueprints.user.model import UserModel
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from annie.blueprints.playground.model import Showcase, Tag
from annie.blueprints.user.model import Submission
from annie.common import user_or_dummy

playground = Blueprint("playground", __name__, template_folder="templates")


@playground.route("/playground")
def overview():
    user = user_or_dummy()
    return render_template(
        "playground.html",
        showcases=Showcase,
        filtered=request.args.get("filtered_by")
        if request.args.get("filtered_by")
        else None,
        user=user,
        tags=Tag.query.all(),
    )


@playground.route("/upvote", methods=["POST"])
def upvote():
    # TODO: Each User can only upvote once per Showcase
    if "showcase_id" in request.form:
        if "token" in session:
            Showcase.upvote(request.form["showcase_id"], session["token"])
            return "OK", 200
        else:
            return "You need to be a logged user to upvote", 401
    else:
        return "Request does not have a showcase_id param", 400


@playground.route("/add_showcase", methods=["POST"])
def add_showcase():
    tags = request.form.getlist("tags[]")
    Showcase(
        name=request.form["title"],
        description=request.form["description"],
        tags=tags,
        submission=Submission.get_by_id(request.form["submission-id"]),
    ).save()
    flash("Sucessfully published your submision!", "success")
    return redirect(url_for("playground.overview"))
