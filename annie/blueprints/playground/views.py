from flask import Blueprint, render_template, request, flash, redirect, url_for
from annie.blueprints.playground.model import Showcase, Tag

playground = Blueprint("playground", __name__, template_folder="templates")


@playground.route("/playground")
def overview():
    return render_template(
        "playground.html",
        showcases=Showcase,
        filtered=request.args.get("filtered_by")
        if request.args.get("filtered_by")
        else None,
    )


@playground.route("/upvote", methods=["POST"])
def upvote():
    # TODO: Each User can only upvote once per Showcase
    try:
        Showcase.upvote(request.form["playground_id"])
        return "OK", 200
    except Exception as e:
        return "Error: " + str(e), 500


@playground.route("/add_showcase", methods=["POST"])
def add_showcase():
    # Check if tag in database or create it if not
    tags = request.form.getlist("tags[]")
    Showcase(
        name=request.form["title"], description=request.form["description"], tags=tags
    ).save()
    flash("Sucessfully published your submision!", "success")
    return redirect(url_for("playground.overview"))
