from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.auth_utils import add_user


registerPage_bp = Blueprint("register", __name__)


@registerPage_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        user_id = request.form.get("user_id")
        username = request.form.get("username")
        password = request.form.get("password")

        if add_user(user_id, username, password):
            flash("회원가입 성공! 로그인하세요.", "success")
            return redirect(url_for("login.login"))
        else:
            flash("이미 존재하는 아이디입니다. 다른 아이디를 사용하세요.", "danger")

    return render_template("register.html")

