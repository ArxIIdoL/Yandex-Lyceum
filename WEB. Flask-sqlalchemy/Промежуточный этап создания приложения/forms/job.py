from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = StringField('Team leader (In the last name, first name format)', validators=[DataRequired()])
    job = TextAreaField('Job', validators=[DataRequired()])
    work_size = StringField('Work size in hour', validators=[DataRequired()])
    collaborators = StringField('Collaborators ids (In this format "1, 2")', validators=[DataRequired()])
    start_date = StringField('Start date (In this format "2025-03-22 17:23:07")')
    end_date = StringField('End date (In this format "2025-03-22 17:23:07")')
    is_finished = BooleanField("Is finished")
    submit = SubmitField('Submit')
