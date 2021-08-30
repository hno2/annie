import os

from flask.helpers import url_for
from annie.common import user_or_dummy
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
import urllib

user = Blueprint("user", __name__, template_folder="templates")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


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
        # Check user token exists in session or request
        if "token" in session:
            auth_token = session["token"]
        elif "auth_token" in request.form:
            auth_token = request.form["auth_token"]
            session["token"] = auth_token
        else:
            return "No user or no user authentication", 400
        user = UserModel.get_by_token_or_404(auth_token)
        assignment = Assignment.get_by_name(urllib.parse.unquote(assignment))
        autograder_path = assignment.path
        if [el.assignment == assignment for el in user.submissions].count(
            True
        ) > assignment.max_submissions - 1:
            return "Maximum Number of submissions", 400
        if "file" not in request.files:
            abort(400, description="No file path")
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(
                shortuuid.uuid() + "." + file.filename.split(".")[1]
            )
            file.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"], "submissions", filename
                )
            )
            submission = Submission(assignment=assignment, filepath=filename)
            db.session.flush()
            submission_id = submission.id
            user.submissions.append(submission)
            user.save()
        else:
            return "Only Python or Python notebook files", 400
    if autograder_path:
        # Add Upload to Queue
        from annie.blueprints.evaluation.tasks import evaluate_submission

        evaluate_submission(filename, autograder_path, submission_id=submission_id)
    return str(submission_id), 200


@user.route("/launch", methods=["GET", "POST"])
@lti(error=error, request="initial", app=current_app)
def launch(lti=lti):
    if request.method == "POST":
        # check if user exists in DB otherwise add him
        if UserModel.get_by_token(request.form["user_id"]) is None:  #
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
    return render_template("index.html", user=user_or_dummy())


@user.app_template_filter("timeago")
def fromnow(date):
    return timeago.format(date, datetime.datetime.now())
