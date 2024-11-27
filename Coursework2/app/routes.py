from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import RegistrationForm, LoginForm, ProfileForm
from app.models import User

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Invalid email or password. Please try again.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.bio = form.bio.data
        current_user.education = form.education.data
        current_user.skills = form.skills.data
        current_user.work_experience = form.work_experience.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))
    return render_template("profile.html", form=form, user=current_user)

@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        confirm_text = request.form.get("confirm_text")
        expected_text = f"Delete-{current_user.name}"

        if confirm_text == expected_text:
            try:
                user = User.query.get(current_user.id)
                db.session.delete(user)
                db.session.commit()
                flash("Your account has been deleted successfully!", "info")
                return redirect(url_for("register"))
            except Exception as e:
                flash("An error occurred while deleting your account. Please try again later.", "danger")
        else:
            flash("Incorrect confirmation text. Account deletion aborted.", "danger")

    return render_template("delete_account.html", user=current_user)
