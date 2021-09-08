import json

from annie.blueprints.playground.model import Showcase
from annie.blueprints.user.model import Assignment, Submission, UserModel
from annie.blueprints.evaluation.model import Comment, Grade
from annie.extensions import db
from flask import current_app, redirect
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.event import listens_for


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

from flask_admin import BaseView, expose


class MyIndexView(BaseView):
    def __init__(self, *args, **kwargs):
        super(MyIndexView, self).__init__(*args, **kwargs)
        self.static_folder = "static"
        self.endpoint = "admin"
        self.name = "Home"

    @expose("/")
    def index(self):
        return self.render(
            "/admin/index.html",
            n_subs=Submission.query.count(),
            n_coms=Comment.query.count(),
            n_show=Showcase.query.count(),
            n_ungraded=Submission.get_all_without_grade(),
        )


admin = Admin(
    name="Annie", template_mode="bootstrap4", index_view=MyIndexView(url="/admin")
)
admin.add_view(ModelView(UserModel, db.session, name="Users", category="Raw Data"))
admin.add_view(FileView(Assignment, db.session, name="Assignment", category="Raw Data"))
admin.add_view(
    ModelView(Submission, db.session, name="Submissions", category="Raw Data")
)
admin.add_view(ModelView(Showcase, db.session, name="Showcases", category="Raw Data"))
admin.add_view(ModelView(Comment, db.session, name="Comments", category="Raw Data"))
admin.add_view(ModelView(Grade, db.session, name="Grades", category="Raw Data"))

if current_app.config["ENABLE_GRADER"]:

    class GraderView(BaseView):
        def filter_ungraded(self, submissions: list[Submission]):
            return [s for s in submissions if s.grade is None]

        @expose("/")
        def index(self):
            # Get all assignments
            assignment_dict = {}
            # count all assignments

            for assignment in Assignment.query.all():

                assignment_dict[assignment.title] = {
                    "count_total": len(assignment.submissions),
                    "count_todo": len(self.filter_ungraded(assignment.submissions)),
                    "gradeable": True if assignment.master_nb else False,
                    "percentag_done": 15,
                }
            return self.render(
                "admin/grader_overview.html", assignments=assignment_dict
            )

    admin.add_view(GraderView(name="Grader", endpoint="graderoverview"))
