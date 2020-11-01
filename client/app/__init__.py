#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

from app import routes
