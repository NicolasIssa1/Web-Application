from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from app.models import User
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
            Regexp(r'^(?=.*[A-Z])(?=.*\d)', message="Password must contain one uppercase letter and one number."),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already registered. Please log in.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    education = TextAreaField('Education', validators=[Length(max=500)])
    skills = TextAreaField('Skills', validators=[Length(max=500)])
    work_experience = TextAreaField('Work Experience', validators=[Length(max=1000)])
    profile_pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'], "Images only!")])
    cover_photo = FileField('Update Cover Photo', validators=[FileAllowed(['jpg', 'png'], "Images only!")])  # New field
    submit = SubmitField('Update Profile')
