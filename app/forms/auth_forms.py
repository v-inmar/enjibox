from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import EmailField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField

from app.models.string_models import UserFirstnameModel, UserEmailModel, UserLastnameModel, UserCurrencyModel


class LoginForm(FlaskForm):
    email = EmailField(label="EmailAddress", validators=[validators.DataRequired()])
    password = PasswordField(label="Password", validators=[validators.DataRequired()])
    remember = BooleanField("Remember Me", default="checked")


class SignUpForm(FlaskForm):
    firstname = StringField(label="Firstname", validators=[validators.DataRequired(), validators.Length(min=1, max=UserFirstnameModel.value_max_length)])
    lastname = StringField(label="Lastname", validators=[validators.DataRequired(), validators.Length(min=1, max=UserLastnameModel.value_max_length)])
    email = EmailField(label="Email Address", validators=[validators.DataRequired(), validators.Length(min=1, max=UserEmailModel.value_max_length)])
    password = PasswordField(label="Password", validators=[validators.DataRequired(), validators.Length(min=8, max=64)])
    repeat = PasswordField(label="Repeat Password", validators=[validators.DataRequired(), validators.EqualTo("password")])
    currency = StringField(label="Currency", validators=[validators.DataRequired(), validators.Length(min=1, max=UserCurrencyModel.value_max_length)])

class RequestVerificationForm(FlaskForm):
    email = EmailField(label="EmailAddress", validators=[validators.DataRequired()])


class ForgotPasswordForm(FlaskForm):
    email = EmailField(label="EmailAddress", validators=[validators.DataRequired()])


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(label="New Password", validators=[validators.DataRequired(), validators.Length(min=8, max=64)])
    repeat_new = PasswordField(label="Repeat New Password", validators=[validators.DataRequired(), validators.EqualTo("new_password")])