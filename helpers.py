import io, sys
import nbformat
from nbconvert import HTMLExporter
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def convertnb(file: str) -> str:
    """Converts a JupyterNotebook to html, by using nbconvert

    Args:
        file (str): File contents

    Returns:
        str: The HTML corresponding with the .ipynb file
    """
    nb = nbformat.reads(file, as_version=4)
    html_exporter = HTMLExporter()
    html_exporter.template_name = "classic"
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
