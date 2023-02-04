from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CircuitForm(FlaskForm):
  circuitCode = TextAreaField('Circuit Code: ',
                      validators=[DataRequired()], render_kw={"placeholder": 'R1 1000_O\nR2 1000_O\nLT S 0.01_A R1,R2,\nPASS LT'})
  submit = SubmitField('Solve')
