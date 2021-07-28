from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import nbformat
from nbconvert import HTMLExporter
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def convert_to_py(filepath: str):
    return filepath


def static_code_check(filepath: str) -> tuple[int, list]:
    """Statically Checks the programming code

    Args:
        filepath (str): A file that has to be checked

    Returns:
        tuple[int, list]: returns a tuple of the score and the list of all messages
    """
    # TODO: Check to not convert .py files

    messages = StringIO()
    reporter = TextReporter(output=messages)
    results = Run(
        ["uploads/" + filepath, "--msg-template='Line {line}: {msg} ({msg_id})"],
        reporter=reporter,
        do_exit=False,
    )  # Change Message format, remove Module test warning,
    print(results.linter.stats)
    score = results.linter.stats["global_note"] * 10
    messages = messages.getvalue().rsplit("\n", 4)[0].split("\n")
    return int(score), messages[1 : len(messages) - 1]


from jinja2 import DictLoader

dl = DictLoader(
    {
        "footer": """
{%- extends '/basic/index.html.j2' -%}

{% block footer %}
FOOOOOOOOTEEEEER
{% endblock footer %}
"""
    }
)


def convert_to_html(content: str) -> tuple[str, list[str]]:
    """Converts a JupyterNotebook to html, by using nbconvert

    Args:
        file (str): File contents

    Returns:
        str: The HTML conversion of the Jupyter NB
        list[str]: List of Classification Results for each code cell
    """
    nb = nbformat.reads(content, as_version=4)
    html_exporter = HTMLExporter(template_file="basic")
    (body, _) = html_exporter.from_notebook_node(nb)
    return body


def hightlightcode(text: str) -> str:
    """Converts a given string with Python syntax to a html string for code hightlighting

    Args:
        text (str): A string containing Python syntax

    Returns:
        str: A html string with pygments classes ready for display in the frontend
    """
    return highlight(text, PythonLexer(), HtmlFormatter(linenos="table"))