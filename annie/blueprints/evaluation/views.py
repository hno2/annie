from flask import Blueprint, render_template, current_app

# from annie.blueprints.evaluation.tasks import get_preds
from annie.blueprints.evaluation.steve import static_code_check, convert_to_html
from nbformat.reader import NotJSONError
from annie.blueprints.playground.model import Tag

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
    try:
        file_data["html"] = convert_to_html(content)
    except NotJSONError:
        return "Something went wrong while formatting"
    if filepath.split(".")[1] == "py":
        score, msgs = static_code_check(filepath)
        file_data["static"] = {"score": score, "msgs": msgs}
    return render_template("evaluation.html", file=file_data, tags=Tag.query.all())
