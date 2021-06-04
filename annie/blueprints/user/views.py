import os

from annie.blueprints.user.model import Assignment, Task, User, db
from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

user = Blueprint("user", __name__, template_folder="templates")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


mock_session = {
    "name": "Foo Bar",
    "mail": "foo.bar@kit.edu",
    "img": "https://randomuser.me/api/portraits/women/72.jpg",
    "tasks": [1, 0, 1, 1, 0, 1, 2],  # 1 sucess, 2 In Progress, 0 unseccessfull
}
mock_lti = {"nickname": "Simon", "lti_id": 42}


@user.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            abort(400, description="No file path")
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = file.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            )
            # TODO: Get ITW Task,
            task = Task(file=filepath, status="0")
            # user = User.query.filter_by(lti.lti_id)

        else:
            return "Only Python or Python notebook files", 400

    ##TODO: Add Upload to Queue and to DB
    return redirect(url_for("eval.home"))


@user.route("/launch", methods=["GET", "POST"])
# @lti(error=error, request="any", app=app)
def launch(lti=mock_lti):
    if request.method == "POST":
        # add user to database
        # check if user exists in DB otherwise add him
        if User.query.filter_by(lti.lti_id) is None:
            user = User(username=lti.nickname, lti_id=lti.lti_id)
        db.session.add(user)
        db.session.commit()
    # TODO: Add finished tasks to session from DB
    session["tasks"] = mock_session["tasks"]
    return render_template("launch.html", lti=lti)
