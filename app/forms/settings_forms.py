from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import EmailField
from wtforms import StringField
from wtforms import PasswordField

from app.models.string_models import UserFirstnameModel, UserLastnameModel, UserEmailModel, UserCurrencyModel


class SettingsNamesForm(FlaskForm):
    firstname = StringField(label="Firstname", validators=[validators.DataRequired(), validators.Length(min=1, max=UserFirstnameModel.value_max_length)])
    lastname = StringField(label="Lastname", validators=[validators.DataRequired(), validators.Length(min=1, max=UserLastnameModel.value_max_length)])

class SettingsEmailForm(FlaskForm):
    email = EmailField(label="Email Address", validators=[validators.DataRequired(), validators.Length(min=1, max=UserEmailModel.value_max_length)])
    password = PasswordField(label="Password", validators=[validators.DataRequired(), validators.Length(min=8, max=64)])

class SettingsPasswordForm(FlaskForm):
    current_password = PasswordField(label="Current Password", validators=[validators.DataRequired()])
    new_password = PasswordField(label="New Password", validators=[validators.DataRequired(), validators.Length(min=8, max=64)])
    repeat_new = PasswordField(label="Repeat New Password", validators=[validators.DataRequired(), validators.EqualTo("new_password")])

class SettingsCurrencyForm(FlaskForm):
    currency = StringField(label="Currency Symbol", validators=[validators.DataRequired(), validators.Length(min=1, max=UserCurrencyModel.value_max_length)])