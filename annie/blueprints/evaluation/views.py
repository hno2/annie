from flask import (
    Blueprint,
    render_template,
    current_app,
    request,
    get_template_attribute,
    session,
)
import markdown
import bleach

# from annie.blueprints.evaluation.tasks import get_preds
from annie.blueprints.evaluation.steve import static_code_check, convert_to_html
from nbformat.reader import NotJSONError
from annie.blueprints.playground.model import Tag
from annie.blueprints.evaluation.model import Comment
from annie.blueprints.user.model import Submission, UserModel


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
    # Get submission Id based on submission filepath
    submission_id = Submission.query.filter_by(filepath=filepath).first().id
    try:
        file_data["html"] = convert_to_html(
            content, Comment.query.filter(Comment.submission_id == submission_id).all()
        )
    except NotJSONError:
        return "Something went wrong while formatting"
    if filepath.split(".")[1] == "py":
        score, msgs = static_code_check(filepath)
        file_data["static"] = {"score": score, "msgs": msgs}
    return render_template(
        "evaluation.html",
        file=file_data,
        tags=Tag.query.all(),
    )


def strip(s: str):
    """strips outer html tags"""

    start = s.find(">") + 1
    end = len(s) - s[::-1].find("<") - 1

    return s[start:end]


@evaluation.post("/addComment")
def add_comment() -> str:
    """Creates a comment for a submission and a given cell_id, returns html of the comment

    Returns:
        [str]: A templated HTML string of the comment
    """
    if "markdown" in request.form:
        html = bleach.clean(  # Sanitize the comment
            strip(
                markdown.markdown(
                    request.form["markdown"],
                )
            )
        )
        if "file" and "cell_id" in request.form:
            comment = Comment(
                markdown=request.form["markdown"],
                html=html,
                submission_id=Submission.query.filter(
                    Submission.filepath.contains(request.form["file"])
                )
                .first()
                .id,
                cell_id=request.form["cell_id"],
                user_id=UserModel.get_by_token(session["token"]).id,
            )
            comment.save()
        else:
            return "Missing file or cell_id", 400
    else:
        return "Missing markdown", 400

    comment_maker = get_template_attribute("_macros.html", "comment")
    return comment_maker(html)
