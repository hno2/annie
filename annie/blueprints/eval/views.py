from flask import Blueprint, render_template, current_app

# from annie.blueprints.eval.tasks import get_preds
from annie.blueprints.eval.steve import static_code_check, convert_to_html

eval = Blueprint("eval", __name__, template_folder="templates")


@eval.get("/review/<filepath>")
def home(filepath):
    with open("uploads/" + filepath, "r") as file:
        content = file.read()
    file_data = {}
    file_data["html"] = convert_to_html(content)
    if filepath.split(".")[1] == "py":
        score, msgs = static_code_check(filepath)
        file_data["static"] = {"score": score, "msgs": msgs}
    return render_template("evaluation.html", file=file_data)
