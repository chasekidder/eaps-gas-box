from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class DataCollectionForm(FlaskForm):
    frequency = IntegerField("Frequency (per sec)", validators=[DataRequired()])
    file_name = StringField("File Name", validators=[DataRequired()])
