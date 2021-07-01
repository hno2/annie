from transformers import *
from fastai.text.all import *

from blurr.data.all import *


def load_model(file: str = "seq_class_learn_export.pkl"):
    learner = load_learner(fname=file)
    return learner


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


if __name__ == "__main__":
    # print(get_preds(["import pandas as pd", "plt.plot('confusion matrix')"]))
    with open("test.ipynb", "r") as file:
        content = file.read()
        get_preds(content)
