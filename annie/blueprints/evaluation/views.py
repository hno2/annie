from config.settings import ENABLE_PROCESS_PREDICTIONS
from annie.blueprints.evaluation.model import Comment, Grade
from annie.blueprints.evaluation.steve import convert_to_html, static_code_check

if ENABLE_PROCESS_PREDICTIONS:
    from annie.blueprints.evaluation.tasks import (
        get_preds,
    )  # Load time can be long as pytorch et al are loaded
from annie.blueprints.playground.model import Tag
from annie.blueprints.user.model import Submission, UserModel
from annie.common import user_or_dummy
from flask import (
    Blueprint,
    current_app,
    get_template_attribute,
    render_template,
    request,
    session,
)


from nbformat.reader import NotJSONError

evaluation = Blueprint("evaluation", __name__, template_folder="templates")


@evaluation.get("/review/<filepath>")
def home(filepath):
    try:
        with open(
            current_app.config["UPLOAD_FOLDER"] + "/submissions/" + filepath, "r"
        ) as file:
            content = file.read()
    except FileNotFoundError:
        return "File not found", 404
    file_data = {}
    # Get submission based on submission filepath
    submission = Submission.query.filter_by(filepath=filepath).first()
    try:
        file_data["html"] = convert_to_html(
            content,
            comments=Comment.query.filter(Comment.submission_id == submission.id).all()
            if not submission.showcase
            else False,  # Show overall comments only if submission is not a showcase
        )
    except NotJSONError:
        return "Something went wrong while formatting"
    # TODO: Check if assignment wants model predictions
    if "process_steps" in submission.grade.__dict__:
        print(submission.grade.process_steps)
        if submission.grade.process_steps != None:
            file_data["process"] = eval(submission.grade.process_steps)  # get from db
    elif (  # TODO: Move this to a celery task
        not submission.grade
        or not submission.grade.process_steps
        and ENABLE_PROCESS_PREDICTIONS
    ):  # if no pogress steps predicted yet, predict them
        file_data["process"] = get_preds(content)
        submission.grade = Grade(process_steps=str(file_data["process"]))
        submission.save()

    if filepath.split(".")[1] == "py":  # If Pyfile uploaded
        score, msgs = static_code_check(filepath)
        file_data["static"] = {"score": score, "msgs": msgs}
    return render_template(
        "evaluation.html",
        file=file_data,
        tags=Tag.query.all(),
        submission=submission,
        user=user_or_dummy(),
        comments=Comment.query.filter_by(submission_id=submission.id).all(),
    )


@evaluation.post("/addComment")
def add_comment() -> str:
    """Creates a comment for a submission and a given cell_id, returns html of the comment

    Returns:
        [str]: A templated HTML string of the comment
    """
    if "markdown" in request.form:
        if "file" in request.form:
            comment = Comment(
                markdown=request.form["markdown"],
                submission_id=Submission.query.filter(
                    Submission.filepath.contains(request.form["file"])
                )
                .first()
                .id,
                cell_id=request.form["cell_id"] if "cell_id" in request.form else None,
                user=UserModel.get_by_token(session["token"]),
            )
            # If not cell_id this is a general comment
            comment.save()
        else:
            return "Missing file or cell_id", 400
    else:
        return "Missing markdown", 400

    comment_maker = get_template_attribute("_macros.html", "comment_block")
    return comment_maker(comment)
