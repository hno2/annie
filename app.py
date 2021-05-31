# app.py
from helpers import convertnb, hightlightcode, get_preds
from steve import static_code_check
from pylti.flask import lti

app = Flask(__name__)
app.config.from_pyfile("config.py")
mock_user = {
    "name": "Foo Bar",
    "mail": "foo.bar@kit.edu",
    "img": "https://randomuser.me/api/portraits/women/72.jpg",
    "tasks": [1, 0, 1, 1, 0, 1, 2],  # 1 sucess, 2 Progress, 0 unseccessfull
}
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


def error(exception):
    """
    Error receives one argument - exception
    exception is a dictionary with the following keys:
        exception['exception'] = lti_exception
        exception['kwargs'] = kwargs - keyword arguments passed to the route
        exception['args'] = args - positional arguments passed to teh route

    :param: exception: `exception` object
    :return: string "HTML in case of exception"
    """
    print(exception)
    return "str(exception)"


@app.route("/launch", methods=["GET", "POST"])
@lti(error=error, request="any", app=app)
def launch(lti):
    return str(lti)


@app.route("/")
def home():
    return render_template(
        "evaluation.html",
        hash=app.config["HASH"],
        user=mock_user,
        file=mock_file,
    )


@app.route("/upload")
def upload():
    return 200


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
