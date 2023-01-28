from flask_wtf import FlaskForm
from wtforms import validators, EmailField, TextAreaField, StringField

from app.models.string_models import UserFirstnameModel, UserLastnameModel, UserEmailModel, ContactMessageModel


class ContactForm(FlaskForm):
    firstname = StringField(label="Firstname", validators=[validators.DataRequired(), validators.Length(min=1, max=UserFirstnameModel.value_max_length)])
    lastname = StringField(label="Lastname", validators=[validators.DataRequired(), validators.Length(min=1, max=UserLastnameModel.value_max_length)])
    email = EmailField(label="Email Address", validators=[validators.DataRequired(), validators.Length(min=1, max=UserEmailModel.value_max_length)])
    message = TextAreaField(label="Message", validators=[validators.DataRequired(), validators.Length(min=1, max=ContactMessageModel.value_max_length)])