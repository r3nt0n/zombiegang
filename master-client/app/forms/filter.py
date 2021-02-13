#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask import Markup

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TimeField, SubmitField, ValidationError
from wtforms.validators import Optional, Length

from app.forms.regexps import validate, ValidRegex, sanitize
from app.data.errors import ErrorMessages


class FilterForm(FlaskForm):
    OS_CHOICES = [
        ('', ''), ('linux', 'linux'), ('windows', 'windows'), ('ios', 'ios'), ('android', 'android')
    ]

    by_username = StringField(u'by username', validators=[Optional()])
    by_os = SelectField(u'by system', validators=[Optional()], choices=OS_CHOICES)
    by_task_type = StringField('by task type', validators=[Optional(), Length(3)])

    by_date_bef = DateField(u'before', validators=[Optional()])
    by_date_aft = DateField(u'after', validators=[Optional()])
    by_time_bef = TimeField(u'', validators=[Optional()], format='%H:%M:%S')
    by_time_aft = TimeField(u'', validators=[Optional()], format='%H:%M:%S')

    filter_btn = SubmitField('🚬  Filter')



    def validate_by_username(self, field):
        if not validate(ValidRegex.Username, field.data):
            raise ValidationError(ErrorMessages.INVALID_USERNAME)
        sanitized_data = str(sanitize(field.data))  # need to escape html because its rendered
        if sanitized_data:
            self.by_username.data = sanitized_data

    def validate_by_task_type(self, field):
        if not validate(ValidRegex.TaskType, field.data):
            raise ValidationError(ErrorMessages.INVALID_TASK_TYPE)
        sanitized_data = str((sanitize(field.data)).lower())  # need to escape html because its rendered
        if sanitized_data:
            self.by_task_type.data = sanitized_data
