import io, sys
import nbformat
from nbconvert import HTMLExporter
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from transformers import *
from fastai.text.all import *

from blurr.data.all import *

inf_learn = load_learner(fname="seq_class_learn_export.pkl")


def get_preds(content: str) -> list[str]:
    """Classifies all code cells of a jupyter nb

    Args:
        content (str): nb content

    Returns:
        list[str]: A list of string with each str corresponding to the classification result for a code cell
    """
    codes = []
    nb_content = json.loads(content)
    for cell in nb_content["cells"]:
        if cell["cell_type"] == "code":  # Only Code Cells
            cell_content = "".join(cell["source"])
            if cell_content != "":  # exclude empty cells
                codes.append(cell_content)
    preds = inf_learn.blurr_predict(codes)
    return preds


def convertnb(content: str) -> tuple[str, list[str]]:
    """Converts a JupyterNotebook to html, by using nbconvert

    Args:
        file (str): File contents

    Returns:
        str: The HTML conversion of the Jupyter NB
        list[str]: List of Classification Results for each code cell
    """
    nb = nbformat.reads(content, as_version=4)
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


if __name__ == "__main__":
    # print(get_preds(["import pandas as pd", "plt.plot('confusion matrix')"]))
    with open("test.ipynb", "r") as file:
        content = file.read()
        get_preds(content)
