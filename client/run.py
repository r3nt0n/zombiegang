#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

#from app import app

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='127.0.0.1')