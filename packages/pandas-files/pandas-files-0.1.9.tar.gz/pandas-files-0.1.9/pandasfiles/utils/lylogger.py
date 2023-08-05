# -*- coding:utf-8 -*-
import logging
import os
__author__ = 'allen'
FORMATTER = '%(asctime)s - %(name)s - %(message)s'


class Lylogger:

    def __init__(self, operate_name, log_file_path,silent=False):
        self.OPERATE_NAME = operate_name
        self.LOG_FILE_PATH = log_file_path

        self.formatter = logging.Formatter(FORMATTER)

        self.logger = logging.getLogger(self.OPERATE_NAME)

        if silent == False:
            self.printing = logging.StreamHandler()
            self.printing.setFormatter(self.formatter)
            self.logger.addHandler(self.printing)

        self.logger.setLevel(logging.DEBUG)
        if self.LOG_FILE_PATH != '':
            self.file = logging.FileHandler(self.LOG_FILE_PATH, mode='w', encoding='utf8')
            self.file.setFormatter(self.formatter)
        self.printf_zero()

    def __set_level__(self, level):
            if level == 'debug':
                self.logger.setLevel(logging.DEBUG)
            elif level == 'info':
                self.logger.setLevel(logging.INFO)
            elif level == 'warning':
                self.logger.setLevel(logging.WARNING)
            elif level == 'error':
                self.logger.setLevel(logging.ERROR)
            elif level == 'critical':
                self.logger.setLevel(logging.CRITICAL)
            else:
                print('set level write current words!')

    def printf_debug(self, *args):

        if args:
            if self.LOG_FILE_PATH != '': self.logger.addHandler(self.file)
            self.logger.debug(*args)

        return True

    def printf_info(self, *args):

        if args:

            if self.LOG_FILE_PATH != '':self.logger.addHandler(self.file)
            self.logger.info(*args)

        return True

    def printf_warning(self, *args):

        if args:

            if self.LOG_FILE_PATH != '':self.logger.addHandler(self.file)
            self.logger.warning(*args)

        return True

    def printf_error(self, *args):

        if args:

            if self.LOG_FILE_PATH != '':self.logger.addHandler(self.file)
            self.logger.error(*args)

        return True

    def printf_critical(self, *args):

        if args:

            if self.LOG_FILE_PATH != '':self.logger.addHandler(self.file)
            self.logger.critical(*args)

        return True

    def printf_zero(self, *args):
        # pass
        if self.LOG_FILE_PATH != '':
            self.file.close()
            if os.path.exists(self.LOG_FILE_PATH):
                if os.path.getsize(self.LOG_FILE_PATH) == 0:
                    os.remove(self.LOG_FILE_PATH)

                return True





def tolog(operate_name,log_file_path='',silent=False):
    f = Lylogger( operate_name,log_file_path,silent=silent)
    return f
