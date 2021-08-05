from flask import session, flash, abort
from annie.blueprints.user.model import UserModel


def user_or_dummy():
    if not "token" in session:
        session["token"] = UserModel.get_by_id(1).auth_token  # Dummy User
        flash("We will use a dummy user, as you have not logged in via a LTI Provider")
    user = UserModel.get_by_token(session["token"])
    if user is None:
        abort(404, "No user with this Auth Token")
    return user
