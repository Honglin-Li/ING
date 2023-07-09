from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('email:', validators=[DataRequired(), Length(5, 64)])
    password = PasswordField('password:', validators=[DataRequired()])

    submit = SubmitField('Log in')


class RegisterFrom(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])

    # personal info
    firstname = StringField('Firstname:', validators=[Length(1, 64)])
    lastname = StringField('Lastname:', validators=[Length(1, 64)])
    is_married = BooleanField('Are you married?')
    share = BooleanField('Share finance state with your partner?')

    submit = SubmitField('Create a new account')


class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField('Old Password:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Change Password')