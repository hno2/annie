import io, sys
from nbconvert.nbconvertapp import main
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def convertnb(file: str) -> str:
    """Converts a JupyterNotebook to html, by using nbconvert

    Args:
        file (str): Filepath to the

    Returns:
        str: The HTML corresponding with the .ipynb file
    """
    argv = ["--template=basic", "--stdout", file]

    capture = io.StringIO()
    sys.stdout = capture  # redirect stdout

    main(argv)

    sys.stdout = sys.__stdout__  # send stdout to normal place again
    out = capture.getvalue()
    print(out)
    return out


def hightlightcode(text: str) -> str:
    """Converts a given string with Python syntax to a html string for code hightlighting

    Args:
        text (str): A string containing Python syntax

    Returns:
        str: A html string with pygments classes ready for display in the frontend
    """
    return highlight(text, PythonLexer(), HtmlFormatter(linenos="table"))
