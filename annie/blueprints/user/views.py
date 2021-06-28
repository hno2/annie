import os

from annie.blueprints.user.model import Assignment, Submission, UserModel, db
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
import timeago, datetime

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


@user.route("/upload/<assignment>", methods=["GET", "POST"])
def upload(assignment):
    if request.method == "POST":
        if "file" not in request.files:
            abort(400, description="No file path")
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        if file and allowed_file(file.filename):
            # TODO: Do not use filename, but random id
            filename = secure_filename(file.filename)
            filepath = file.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            )
            # TODO: Get username from auth request
            user = UserModel.find_by_username(session["name"])
            cur_assign = Assignment.find_by_name(assignment)
            user.submissions.append(Submission(assignment=cur_assign))
            user.save()

        else:
            return "Only Python or Python notebook files", 400

    ##TODO: Add Upload to Queue and to DB
    return "Uploaded and Added", 200


@user.route("/launch", methods=["GET", "POST"])
# @lti(error=error, request="any", app=app)
def launch(username="Simon Klug"):
    if request.method == "POST":
        # check if user exists in DB otherwise add him
        if UserModel.find_by_username(userid) is None:
            user = UserModel(username=lti.nickname, lti_id=lti.lti_id)

    # Get Current User
    user = UserModel.find_by_username(username)
    session["name"] = user.username
    return render_template(
        "launch.html",
        assignments=user.assignments,
        submissions=user.submissions,
    )


@user.app_template_filter("timeago")
def fromnow(date):
    return timeago.format(date, datetime.datetime.now())
