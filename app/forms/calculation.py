from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class FinanceForm(FlaskForm):
    # income
    salary = IntegerField('Salary:', default=0)
    external_income = IntegerField('External income:', default=0)

    # expense
    rent = IntegerField('Rent:', default=0)
    load = IntegerField('Load & Credit:', default=0)
    travel = IntegerField('Travel:', default=0)
    insurance = IntegerField('Insurance:', default=0)
    education = IntegerField('Education:', default=0)
    personal_care = IntegerField('Personal care:', default=0)

    # by hour
    childcare = IntegerField('Paid child care:', default=0)
    household = IntegerField('Paid household:', default=0)

    childcare_hours = IntegerField('Child care hours on own:', default=0)
    household_hours = IntegerField('Household hours on own:', default=0)

    submit = SubmitField('Submit')