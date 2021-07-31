from sqlalchemy.event import listens_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, form
from annie.blueprints.user.model import UserModel, Assignment, Submission
from flask import current_app
from annie.extensions import db
from annie.blueprints.playground.model import Showcase


class FileView(ModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {"path": form.FileUploadField}

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        "path": {
            "label": "Autograder ZIP",
            "base_path": current_app.config["UPLOAD_FOLDER"] + "/assignments/master/",
            "allow_overwrite": True,
            "allowed_extensions": ["zip"],
        }
    }


# # Hook once a Notebook is uploaded, generate student version
# @listens_for(Assignment.path, "set", propagate=True)
# def _assignment_path_changed(target, value, _, initiator):
#     print(value)
#     if value is not None:
#         generate_student_nb(
#             current_app.config["UPLOAD_FOLDER"] + "/asåsignments/master/" + value
#         )


admin = Admin(name="Annie", template_mode="bootstrap4")
admin.add_view(ModelView(UserModel, db.session, name="Users"))
admin.add_view(FileView(Assignment, db.session, name="Assignment"))
admin.add_view(ModelView(Submission, db.session, name="Submissions"))
admin.add_view(ModelView(Showcase, db.session, name="Showcases"))
