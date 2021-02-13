#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from app.models.data import Data


class Master(Data):
    def __init__(self):
        super().__init__()
        self.name = 'master'
        self.id = ''
        self.username = ''
        self.public_key = ''


    def create(self):
        data['username']
        self.username = request.form.get('username')
        self.public_key = request.form.get('public_key')

        Data.create(self)

    def update(self, request):
        self.public_key = request.form.get('public_key')
        Data.update(self, request)