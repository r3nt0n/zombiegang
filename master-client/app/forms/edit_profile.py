#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, SubmitField, ValidationError

from app.forms.extra_validators import RequiredIf
from app.forms.regexps import validate, ValidRegex
from app.data.errors import ErrorMessages

class EditProfileForm(FlaskForm):
    pswd_btn = SubmitField('🗝️ Update password')
    password = PasswordField('password', validators=[RequiredIf('pswd_btn')])
    public_key_btn = SubmitField('🔒 Update public key')
    public_key = TextAreaField('public key', validators=[RequiredIf('public_key_btn')])


    def validate_password(self, field):
        if not validate(ValidRegex.Password, field.data):
            raise ValidationError(ErrorMessages.INVALID_PASSWORD)
        sanitized_data = str(field.data)
        if sanitized_data:
            self.password.data = sanitized_data

    def validate_public_key(self, field):
        # ...
        # ...
        pass
