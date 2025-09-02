from flask import Blueprint, render_template

profile_bp = Blueprint("user_profile", __name__)


@profile_bp.route("/profile")
def make_profile():
    return render_template("user/mypage.html")

