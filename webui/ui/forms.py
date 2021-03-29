from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class CycleConfigForm(FlaskForm):
    frequency = IntegerField("Frequency (per sec)", validators=[DataRequired()])
    duration = IntegerField("Duration (min)", validators=[DataRequired()])
    site_id = 0
    # somehow add a selector and adder for new sites

class AddSensorForm(FlaskForm):
    name = StringField("File Name", validators=[DataRequired()])
    address = StringField("File Name", validators=[DataRequired()])
    data_type_id = 0
    # somehow add a selector and adder for new data_types

