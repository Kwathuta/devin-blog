from flask import render_template, redirect, url_for, flash, request
from . import auth
from ..models import User
from .forms import RegistrationForm, LoginForm
from .. import db
from flask_login import login_user, login_required, logout_user
from ..email import mail_message


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    title = "New Account"

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()

        mail_message(
            "Welcome to 60 Seconds Impressions!", "email/welcome", user.email, user=user
        )

        return redirect(url_for("auth.signin"))
    return render_template("auth/signup.html", registration_form=form, title=title)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get("next") or url_for("main.index"))

        flash("Invalid username or Password")

    title = "60-seconds impressions login"
    return render_template("auth/signin.html", login_form=login_form, title=title)


@auth.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for("main.index"))
