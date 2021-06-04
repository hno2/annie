from flask import Blueprint, render_template, current_app
from annie.blueprints.eval.tasks import convertnb, get_preds

eval = Blueprint("eval", __name__, template_folder="templates")

# Data Structure for Files, will be transferred to DB Class soon
with open("test.ipynb", "r") as file:
    content = file.read()
    score, msgs = 50, ["no_message"]  # static_code_check("test.py")
    html = convertnb(content)
    mock_file = {
        "html": html,
        "static": {"score": score, "msgs": msgs},
        "process": get_preds(content),
    }


@eval.get("/")
def home():
    return render_template(
        "evaluation.html",
        hash=current_app.config["HASH"],
        file=mock_file,
    )
