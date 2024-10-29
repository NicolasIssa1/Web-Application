from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms import BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from datetime import datetime


class AssessmentForm(FlaskForm):
    # these are the forms to addd or edit our assesments
    title = StringField('Title', validators=[DataRequired()])
    module_code = StringField('Module Code', validators=[DataRequired()])
    deadline_date = DateField('Deadline Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    is_complete = BooleanField('Is Complete')
    submit = SubmitField('Submit')

    def validate_deadline_date(self, deadline_date):
        # in case the deadline date is in the past, raise an error
        if deadline_date.data < datetime.today().date():
            raise ValidationError('The deadline date cannot be in the past.')
