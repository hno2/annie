# app.py
from flask import Flask, render_template
from helpers import convertnb, hightlightcode
from steve import static_code_check

app = Flask(__name__)
app.config.from_pyfile("config.py")
mock_user = {
    "name": "Foo Bar",
    "mail": "foo.bar@kit.edu",
    "img": "https://randomuser.me/api/portraits/women/72.jpg",
    "tasks": [1, 0, 1, 1, 0, 1, 2],  # 1 sucess, 2 Progress, 0 unseccessfull
}
# Data Structure for Files, will be transferred to DB Class soon
with open("test.py", "r") as file:
    code = file.read()
score, msgs = static_code_check("test.py")
mock_file = {
    "code": code,
    "html": hightlightcode(code),
    "static": {"score": score, "msgs": msgs},
}


@app.route("/")
def home(nb=False):
    with open("test.py", "r") as file:
        code = hightlightcode(file.read())
    if nb:
        code = convertnb("test.ipynb")
    return render_template(
        "evaluation.html",
        code=code,
        hash=app.config["HASH"],
        user=mock_user,
        file=mock_file,
    )


@app.route("/upload")
def upload():
    return 200


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
