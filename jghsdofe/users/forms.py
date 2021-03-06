from flask import url_for
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, ValidationError, EqualTo, Length
from jghsdofe.models import User
from jghsdofe import bcrypt

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=32, message='Password must be 32 or fewer characters long.')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Password and Confirm Password must be identical. Note that passwords are case-sensitive.')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError(f'An account with that username already exists. If you already have an account please <a href="{url_for("users.login")}">log in</a>.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=8, message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm New Password', validators=[InputRequired(), EqualTo('password', message='Password and Confirm Password must be identical. Note that passwords are case-sensitive.')])
    submit = SubmitField('Change Password')

    def validate_current_password(self, current_password):
        if not bcrypt.check_password_hash(current_user.password, current_password.data):
            raise ValidationError('Current password incorrect. Please try again. If you have forgotten it please email neelu.rsa@gmail.com for assistance.')
