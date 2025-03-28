from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    chief = StringField('Chief (In the last name, first name format)', validators=[DataRequired()])
    members = StringField('Members ids (In this format "1, 2")', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
