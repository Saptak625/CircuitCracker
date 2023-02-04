from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CircuitForm(FlaskForm):
  circuitCode = TextAreaField('Circuit Code: ',
                      validators=[DataRequired()], render_kw={"placeholder": 'R1 1000_O\nR2 1000_O\nLT S 0.01_A R1,R2,\nPASS LT'})
  roundingPlace = IntegerField('Rounding Decimal Places: ', default=5, validators=[DataRequired(), NumberRange(min=0)])
  showVoltage = BooleanField('Show Voltage', default='checked')
  showCurrent = BooleanField('Show Current', default='checked')
  showResistance = BooleanField('Show Resistance', default='checked')
  showLegs = BooleanField('Show Legs', default='checked')
  showResistors = BooleanField('Show Resistors', default='checked')
  
  submit = SubmitField('Solve')
