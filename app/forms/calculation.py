from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField


class FinanceForm(FlaskForm):
    # career
    goal = RadioField('Your Goal as a partner:',
                      choices=[('0','Financial Priority'),('1','Life Priority')])

    # income
    salary = IntegerField('Net Salary:', default=0)
    salary_per_hour = IntegerField('Salary per Hour:', default=0)

    # expense
    expenses_contribution = IntegerField('Expense:', default=0)
    house_care_hours_per_day = IntegerField('Care Work Hours a Day:', default=0)

    # time distribution
    #working_hours_a_day = IntegerField('Work Hours a Day:', default=0)
    #care_hours_a_day = IntegerField('Care Hours a Day:', default=0)
    #life_hours_a_day = IntegerField('Life Hours a Day:', default=0)


    submit = SubmitField('Check Finance State')


class PartnerFinanceForm(FlaskForm):
    # income
    salary = IntegerField('Net Salary:', default=5500)
    salary_per_hour = IntegerField('Salary per Hour:', default=35)

    # expense
    expenses_contribution = IntegerField('Expense:', default=2100)
    house_care_hours_per_day = IntegerField('Care Work Hours a Day:', default=0)

    submit = SubmitField('Check Fair Share')