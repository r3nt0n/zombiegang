#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from app import zombie

if __name__ == "__main__":
    while True:
        try:
            zombie.run()

        except KeyboardInterrupt:
            from app.components import logger
            logger.log('manual exit requested \n\nPRESS Ctrl+C again...', 'CRITICAL')
            break

        except Exception as e:
            from app.components import logger
            logger.log('CRITICAL ERROR: {}'.format(e), 'CRITICAL')
            logger.log('trying to restart connection', 'INFO')
            continue
