#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired

from app.forms.regexps import validate, ValidRegex, sanitize
from app.data.errors import ErrorMessages

class LoginForm(FlaskForm):
    remote_host = StringField('remote host', validators=[InputRequired(message=ErrorMessages.REQUIRED_FIELD)])
    username = StringField('username', validators=[InputRequired(message=ErrorMessages.REQUIRED_FIELD)])
    password = PasswordField('password', validators=[InputRequired(message=ErrorMessages.REQUIRED_FIELD)])
    create_btn = SubmitField('Create user')
    login_btn = SubmitField('Login')

    def validate_remote_host(self, field):
        if ((not validate(ValidRegex.Hostname, field.data)) and (not validate(ValidRegex.IpAddress, field.data)) and
            (not validate(ValidRegex.HostPort, field.data)) and (not validate(ValidRegex.IpPort, field.data))):
            raise ValidationError(ErrorMessages.INVALID_HOSTNAME)
        sanitized_data = str(sanitize(field.data))  # need to escape html because its rendered
        if sanitized_data:
            self.remote_host.data = sanitized_data

    def validate_username(self, field):
        if not validate(ValidRegex.Username, field.data):
            raise ValidationError(ErrorMessages.INVALID_USERNAME)
        sanitized_data = str(sanitize(field.data))  # need to escape html because its rendered
        if sanitized_data:
            self.username.data = sanitized_data

    def validate_password(self, field):
        if not validate(ValidRegex.Password, field.data):
            raise ValidationError(ErrorMessages.INVALID_PASSWORD)
        sanitized_data = str(field.data)
        if sanitized_data:
            self.password.data = sanitized_data
