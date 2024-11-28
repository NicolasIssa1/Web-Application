import os
import secrets
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import RegistrationForm, LoginForm, ProfileForm
from app.models import User
from PIL import Image

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to save pictures (profile and cover)
def save_picture(form_picture, folder='profile_pics'):
    """Save uploaded picture and return the filename."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, f'static/{folder}', picture_fn)

    # Resize image based on type (profile/cover)
    output_size = (300, 300) if folder == 'profile_pics' else (1200, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# Check if uploaded file is allowed
def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
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
    return redirect(url_for("home"))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        # Handle profile picture upload
        if form.profile_pic.data:
            if not allowed_file(form.profile_pic.data.filename):
                flash("Invalid profile picture format. Allowed: PNG, JPG, JPEG, GIF.", "danger")
                return redirect(url_for("profile"))
            picture_file = save_picture(form.profile_pic.data, 'profile_pics')
            current_user.profile_pic = picture_file

        # Handle cover photo upload
        if form.cover_photo.data:
            if not allowed_file(form.cover_photo.data.filename):
                flash("Invalid cover photo format. Allowed: PNG, JPG, JPEG, GIF.", "danger")
                return redirect(url_for("profile"))
            cover_file = save_picture(form.cover_photo.data, 'cover_photos')
            current_user.cover_photo = cover_file

        # Update other fields
        current_user.name = form.name.data
        current_user.bio = form.bio.data
        current_user.education = form.education.data
        current_user.skills = request.form.get("skills", "")
        current_user.work_experience = form.work_experience.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    # Ensure existing profile and cover photo are displayed
    profile_pic_url = url_for('static', filename=f'profile_pics/{current_user.profile_pic}') if current_user.profile_pic else None
    cover_photo_url = url_for('static', filename=f'cover_photos/{current_user.cover_photo}') if current_user.cover_photo else None

    # Safely handle skills
    skills = current_user.skills.split(',') if current_user.skills else []

    return render_template("profile.html", form=form, user=current_user, profile_pic_url=profile_pic_url, cover_photo_url=cover_photo_url, skills=skills)

@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        # Get confirmation text from the form
        confirm_text = request.form.get("confirm_text", "").strip()
        expected_text = f"Delete-{current_user.name}"  # Expected text to match

        if confirm_text == expected_text:
            try:
                user = User.query.get(current_user.id)

                # Remove profile picture file if it exists
                if user.profile_pic:
                    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', user.profile_pic)
                    if os.path.exists(picture_path):
                        os.remove(picture_path)

                # Remove cover photo file if it exists
                if user.cover_photo:
                    cover_path = os.path.join(current_app.root_path, 'static/cover_photos', user.cover_photo)
                    if os.path.exists(cover_path):
                        os.remove(cover_path)

                db.session.delete(user)
                db.session.commit()
                flash("Your account has been deleted successfully!", "info")
                return redirect(url_for("register"))
            except Exception as e:
                flash("An error occurred while deleting your account. Please try again later.", "danger")
        else:
            flash("Incorrect confirmation text. Account deletion aborted.", "danger")

    return render_template("delete_account.html", user=current_user)

@app.route("/profile/inline_edit", methods=["POST"])
@login_required
def inline_edit():
    """Handle inline edits for user profile fields."""
    data = request.get_json()
    field = data.get("field")
    value = data.get("value")

    if field not in ["name", "bio", "education", "skills", "work_experience"]:
        return jsonify({"success": False, "message": "Invalid field."}), 400

    try:
        setattr(current_user, field, value)
        db.session.commit()
        return jsonify({"success": True, "message": f"{field} updated successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred. Please try again later."}), 500

@app.route("/network")
@login_required
def network():
    return render_template("network.html")

@app.route('/jobs')
@login_required
def jobs():
    return render_template("jobs.html")
