import os
from flask import Blueprint, request, redirect, current_app
from typing import *


from annie.blueprints.user.model import Assignment, Submission
from annie.blueprints.evaluation.model import Grade

from grader.lama_grading_helper.frontend.grading import (
    GradingView,
    Notebook,
    NotebookFile,
)
from grader.lama_grading_helper import (
    DATA_PATH,
    WORKSPACE_DIR_NAME,
    TEST_BATCH_DIR_NAME,
)
from grader.lama_grading_helper.backend import Workspace

workspace = Workspace(os.path.join(DATA_PATH, WORKSPACE_DIR_NAME))


grader = Blueprint(
    "grader",
    __name__,
    template_folder="/Users/simon/Desktop/Masterarbeit/code/annie/grader/lama_grading_helper/templates",
    url_prefix="/grader",
    static_folder="/Users/simon/Desktop/Masterarbeit/code/annie/grader/lama_grading_helper/static",
)


def filter_ungraded(submissions: list[Submission]):
    return [s for s in submissions if s.grade is None]


def get_master_path(assignment: str):
    master_path = (
        current_app.config["UPLOAD_FOLDER"]
        + "/assignments/master/"
        + Assignment.get_by_name(assignment).master_nb
    )
    return master_path


def get_submission_path(path: str):
    return current_app.config["UPLOAD_FOLDER"] + "/submissions/" + path


@grader.app_template_filter("balance_closing_tags_hacky")
def balance_closing_tags_hacky(html: str, tags: Iterable[str] = ["b"]) -> str:
    # Sometimes html tags are not closed in our notebooks. This mostly isn't a problem, unless those are formatting tags such as <b> or <i>, as these will damage the formatting of the rest of the page.
    # Luckily, html is not a regular language and parsers are so tolerant that we can just add the closing tags at the end of our string, disregarding XML hierarchy, without failing, and, most importantly, without changing the format inside the cell
    for tag in tags:
        tag_diff = html.count(f"<{tag}>") - html.count(f"</{tag}>")
        if tag_diff > 0:
            for i in range(tag_diff):
                html += f"</{tag}>"
    return html


@grader.get("/<assignment>/")
def index(assignment):
    # Redirect to first notebook to grade
    return redirect(
        "/grader/"
        + assignment
        + "/"
        + filter_ungraded(Assignment.get_by_name(assignment).submissions)[0].filepath
    )


@grader.get("/<assignment>/<gradingnb>")
def nb_compare(gradingnb, assignment):
    """Create two Notebook classes for reference and student"""
    master_nb = Assignment.get_by_name(assignment).master_nb
    if master_nb is not None:
        get_master_path(assignment)
        reference = Notebook.from_file(NotebookFile(get_master_path(assignment)))
    else:
        return "You must define a master_nb to use the grader"
    student = Notebook.from_file(NotebookFile(get_submission_path(gradingnb)))
    gradingview = GradingView(reference, student)
    return gradingview.to_html()


@grader.route("/update/<path:path>", methods=["POST"])
def update_grading(path: str):  # update grading only if prog=100%
    assignment, notebook_uuid = path.split("/")
    data = request.json
    nb_file = NotebookFile(get_submission_path(notebook_uuid))
    grading = nb_file.get_grading()

    if "grade" in data:  # Overall Grade, seems to be never set
        try:
            grading.grade = int(data["grade"])
        except:
            grading.grade = None

    if "comment" in data:
        try:
            grading.comment = data["comment"]
        except:
            grading.comment = ""

    if "cells" in data:
        for i_cell, cell_data in data["cells"].items():
            if "rating" in cell_data:
                try:
                    cell_data["rating"] = cell_data["rating"]
                except:
                    pass
            grading.cells[int(i_cell)] = cell_data

    nb_file.overwrite_grading(grading)
    if Notebook.from_file(nb_file).compute_grading_progress() == 1.0:
        ## Save Grade
        sub = Submission.get_by_filepath(notebook_uuid)
        if sub.grade == None:
            sub.grade = Grade(
                manual=int(grading.grade / 30 * 100)
            )  # TODO: Should be 0..100, weighted by points
        else:
            sub.grade.manual = int(grading.grade / 30 * 100)
        sub.save()

    return ""
