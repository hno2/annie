from flask import Blueprint, render_template, current_app

# from annie.blueprints.eval.tasks import get_preds
from annie.blueprints.eval.steve import static_code_check, convert_to_html
from nbformat.reader import NotJSONError

eval = Blueprint("eval", __name__, template_folder="templates")


@eval.get("/review/<filepath>")
def home(filepath):
    with open(
        current_app.config["UPLOAD_FOLDER"] + "/submissions/" + filepath, "r"
    ) as file:
        content = file.read()
    file_data = {}
    try:
        file_data["html"] = convert_to_html(content)
    except NotJSONError:
        return "Something went wrong while formatting"
    if filepath.split(".")[1] == "py":
        score, msgs = static_code_check(filepath)
        file_data["static"] = {"score": score, "msgs": msgs}
    return render_template("evaluation.html", file=file_data)
