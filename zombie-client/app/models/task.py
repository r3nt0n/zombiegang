#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

from datetime import datetime

from app.components import logger
from app.modules import crud

class Task:
    def __init__(self, data):
        self.id = data['id']
        self.task_type = data['task_type']
        self.task_content = data['task_content']
        self.to_exec_at = data['to_exec_at']
        self.to_stop_at = data['to_stop_at']
        self.manual_stop = data['manual_stop']

        self.mission_id = data['mission_id']
        self.read_confirm = data['read_confirm']
        self.running = data['running']
        self.result = data['result']
        self.exec_at = data['exec_at']
        self.mission_manual_stop = data['mission_manual_stop']

    # update read confirm
    def report_is_read(self):
        self.read_confirm = "true"
        updated = crud.update_data('mission', {
            'id': self.mission_id,
            'read_confirm': self.read_confirm
        })
        if not updated:
            return False
        return updated

    def report_is_starting(self):
        self.running = "true"
        updated = crud.update_data('mission', {
            'id': self.mission_id,
            'running': self.running
        })
        if not updated:
            return False
        return updated
    
    def start(self):
        # this is the method to extend with custom code
        pass

    def keep_reading_manual_stop(self):
        logger.log('starting thread to keep reading manual_stop for {}'.format(self), 'OTHER')
        while True:
            data = crud.read_data('missions', {"id": self.mission_id})
            if data and ("manual_stop" in data) and (data["manual_stop"] != self.mission_manual_stop):
                self.mission_manual_stop = data["manual_stop"]
                logger.log('manual_stop updated: {}'.format(self.mission_manual_stop), 'WARNING')

            #if (self.mission_manual_stop != 'false') or (self.running == 'false') or self.result:
            if (self.mission_manual_stop != 'false') or (self.running == 'false' and self.result):
                logger.log('finishing manual stop thread, {} is completed'.format(self), 'OTHER')
                break

    def report_result(self):
        #self.result = "command output example"
        # self.result should be assigned at the end of custom start methods, collecting task outputs
        updated = crud.update_data('mission', {
            'id': self.mission_id,
            'result': self.result,
            'running': self.running,
            'exec_at': self.exec_at
        })
        if not updated:
            logger.log('error while trying to update result: {}'.format(self.result), 'ERROR')
            return False
        logger.log('result task updated: {}'.format(self.result), 'SUCCESS')
        return updated

    def run(self):
        # update running field
        self.report_is_starting()
        logger.log('task {} has REPORT is about to start...'.format(self), 'INFO')
        while True:
            # manual stop controller
            if self.manual_stop != 'false':
                break
            # execute task
            self.start()
            logger.log('task {} is starting...'.format(self), 'INFO')
            try:
                # stop by to_stop_at field
                stop_time = datetime.strptime(self.to_stop_at, '%Y-%m-%d %H:%M:%S')
                #logger.log('Task.to_stop_at: {}'.format(self.to_stop_at), 'DEBUG')
                #logger.log('stop_time: {}'.format(stop_time), 'ERROR')
                #logger.log('datetime.now() >= stop_time: {}'.format((datetime.now() >= stop_time)), 'ERROR')
                if datetime.now() >= stop_time:
                    logger.log('stop_time reached: {}'.format(stop_time), 'ERROR')
                    break
            except (ValueError, TypeError) as e:
                logger.log('error while trying to read task.to_stop_at: {}'.format(e), 'ERROR')
                logger.log('task.to_stop_at: {}'.format(self.to_stop_at), 'ERROR')
                break
        # update result and exec_at fields
        logger.log('task {} is finished'.format(self, 'INFO'))
        self.running = 'false'
        self.exec_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #self.report_result()
        return True

    def __repr__(self):
        return '<' + type(self).__qualname__ + ' {id: '+str(self.id)+', mission_id: '+str(self.mission_id)+ '}>'

