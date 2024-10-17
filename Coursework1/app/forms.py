from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    module_code = StringField('Module Code', validators=[DataRequired()])
    deadline_date = DateField('Deadline Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    is_complete = BooleanField('Is Complete')
    submit = SubmitField('Add Assessment')
