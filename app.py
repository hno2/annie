# app.py
from flask import Flask, render_template
from helpers import convertnb, hightlightcode

app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/")
def home(nb=False):
    with open("test.py", "r") as file:
        code = hightlightcode(file.read())
    if nb:
        code = convertnb("test.ipynb")
    return render_template("evaluation.html", code=code, hash=app.config["HASH"])


@app.route("/upload")
def upload():
    return 200


app.run(debug=True)
