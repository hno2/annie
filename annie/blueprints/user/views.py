import os

from flask.helpers import url_for

from annie.blueprints.user.model import Assignment, Submission, UserModel, db
from flask import (
    Blueprint,
    abort,
    current_app,
    render_template,
    request,
    session,
    flash,
)
from pylti.flask import lti
import shortuuid
from werkzeug.utils import redirect, secure_filename
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


def error(exception=None):
    """render error page
    :param exception: optional exception
    :return: the error.html template rendered
    """
    print(exception)
    return str(exception)


@user.route("/upload/<assignment>", methods=["GET", "POST"])
def upload(assignment):
    if request.method == "POST":
        if "file" not in request.files:
            abort(400, description="No file path")
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        if file and allowed_file(file.filename):

            filename = secure_filename(
                shortuuid.uuid() + "." + file.filename.split(".")[1]
            )

            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            if "username" in session:
                print("username")
                user = UserModel.find_by_username(session["username"])
            elif request.form["auth_token"]:
                print("auth_token")
                user = UserModel.find_by_token(request.form["auth_token"])
            else:
                return
            user.submissions.append(
                Submission(
                    assignment=Assignment.find_by_name(assignment), filepath=filename
                )
            )
            user.save()

        else:
            return "Only Python or Python notebook files", 400

    ##TODO: Add Upload to Queue
    return "Uploaded and Added", 200


@user.route("/launch", methods=["GET", "POST"])
@lti(error=error, request="initial", app=current_app)
def launch(lti=lti):
    if request.method == "POST":
        # check if user exists in DB otherwise add him
        if UserModel.find_by_token(request.form["user_id"]) is None:  #
            user = UserModel(
                username=request.form["lis_person_name_full"],
                auth_token=request.form["user_id"],
                assignments=Assignment.query.all(),  # TODO: How to add Standard Assignments
            )
            user.save()
            flash("A new user based on the LTI Data was created")
        session["token"] = request.form["user_id"]
        session["return_url"] = request.form["launch_presentation_return_url"]
    return redirect(url_for("user.main"))


@user.route("/", methods=["GET", "POST"])
def main():
    if not "user_id" in session:
        session["token"] = UserModel.find_by_id(1).auth_token  # Dummy User
        flash("We will use a dummy user, as you have not logged in via a LTI Provider")
    user = UserModel.find_by_token(session["token"])
    print(session["token"])
    if user is None:
        abort(404, "No user with this Auth Token")

    return render_template(
        "launch.html",
        user=user,
        assignments=user.assignments,
        submissions=user.submissions,
    )


@user.app_template_filter("timeago")
def fromnow(date):
    return timeago.format(date, datetime.datetime.now())
