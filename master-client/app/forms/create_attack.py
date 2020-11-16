#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, TimeField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Optional

from app import logger
from app.forms.regexps import validate, ValidRegex
from app.data.errors import ErrorMessages


class CreateTaskForm(FlaskForm):
    task_name = StringField(u'task name', validators=[InputRequired()])
    to_exec_at_date = DateField(u'', validators=[Optional()])
    to_exec_at_time = TimeField(u'', validators=[Optional()], format='%H:%M:%S')
    enable_start_dt = BooleanField(u'⏲️  start at:', validators=[Optional()])
    to_stop_at_date = DateField(u'', validators=[Optional()])
    to_stop_at_time = TimeField(u'', validators=[Optional()], format='%H:%M:%S')
    enable_stop_dt = BooleanField(u'⏲️  stop at:', validators=[Optional()])
    create_btn = SubmitField('⚔️  Attack')

    # def validate_to_exec_at_time(self, field):
    #     logger.log('to_exec_at_time: {}'.format(field.data), 'QUESTION')

class CreateDDosAttackForm(CreateTaskForm):
    DOS_CHOICES = [('slowloris', 'slowloris'), ('rudy', 'RUDY'), ('syn', 'SYN flood')]
    target = StringField(u'target', validators=[InputRequired()])
    attack_type = SelectField(u'attack type', validators=[InputRequired()], choices=DOS_CHOICES)

    def validate_target(self, field):
        if (not validate(ValidRegex.IpAddress, field.data) and not validate(ValidRegex.Hostname, field.data) and
            not validate(ValidRegex.IpPort, field.data) and not validate(ValidRegex.HostPort, field.data)):
            raise ValidationError(ErrorMessages.INVALID_TARGET)
        sanitized_data = str(field.data)  # need to escape html because its rendered
        if sanitized_data:
            self.target.data = sanitized_data


class CreateBruteAttackForm(CreateTaskForm):
    BRT_CHOICES = [('ssh', 'ssh'), ('http', 'http(s)'), ('ftp', 'ftp')]
    target = StringField(u'target', validators=[InputRequired()])
    attack_type = SelectField(u'service', validators=[InputRequired()], choices=BRT_CHOICES)