from enum import auto
from annie.app import create_celery_app
from otter.api import grade_submission
from flask import current_app
from annie.blueprints.user.model import Submission, Grade

celery = create_celery_app()


@celery.task()
def evaluate_submission(
    notebook_path: str, autograder_file: str, submission_id: int
) -> None:
    submission = Submission.get_by_id(submission_id)
    print("id: ", submission_id, " submission: ", submission)
    results = evaluate_static(
        current_app.config["UPLOAD_FOLDER"] + "/submissions/" + notebook_path,
        current_app.config["UPLOAD_FOLDER"] + "/assignments/master/" + autograder_file,
    )
    if submission.grade is None:
        submission.grade = Grade(
            static=(results.total / results.possible) * 100,
            overall=(results.total / results.possible) * 100,
        )
        print(submission.grade)
    else:
        submission.grade.static = results.total / results.possible
        # submission.grade.update_overall()
    submission.save()
    return None


def evaluate_static(notebook_path: str, autograder_file: str):
    results = grade_submission(autograder_file, notebook_path, quiet=True)
    return results
