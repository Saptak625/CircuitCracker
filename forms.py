from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
  inputString = StringField('Input: ',
                      validators=[DataRequired()], render_kw={"placeholder": "This is a placeholder."})
  submit = SubmitField('🔎')
