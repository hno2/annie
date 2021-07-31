from flask import Blueprint, render_template, request


clippy = Blueprint("clippy", __name__, template_folder="templates")


@clippy.get("/recommend")
def recommend():
    return render_template(
        "recommend.html",
        messages=[
            {"message": "hello", "type": "clippy"},
            {"message": "Hey there", "type": "user"},
        ],
    )
