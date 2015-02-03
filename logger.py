# -*- coding: utf-8 -*-
import logging
import os
from datetime import date
from settings import Settings

__author__ = 'Sencer Hamarat'


class Logger:
    def __init__(self, log_name, level='INFO', log_dir='logs', log_format=None, handler=None):
        """
        log_name: log file name
        level: log levels: CRITICAL, ERROR, WARNING, INFO, DEBUG
        log_dir: log folder. default <project_folder>/logs/
        log_format: logging format
        handler: TODO (incomplete)
        """
        self.log_name = log_name
        self.loger = None
        self.formatter = None
        self.handler = handler
        self.level = 'INFO'
        self.log_format = u"%(asctime)s %(levelname)s %(name)s %(process)d %(threadName)s %(module)s: " \
                          u"%(lineno)d %(funcName)s() %(message)s\r\n"
        self.__configure_level(level.upper())
        self.__configure_format(log_format)
        self.__configure_handler(log_dir)

    def __configure_level(self, level):
        if level not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
            raise Exception(u"{} geçerli bir log seviyesi değil".format(level))
        self.level = 'DEBUG' if Settings.DEBUG else level

    def __configure_format(self, log_format):
        if log_format:
            self.log_format = log_format
        self.formatter = logging.Formatter(self.log_format)

    def __configure_handler(self, log_dir):
        _dir = '{}/{}'.format(Settings.PROJECT_ROOT, log_dir)
        if not os.path.exists(_dir):
            os.mkdir(_dir)
        _filename = "{}/{}.log".format(_dir, self.log_name)
        self.handler = logging.FileHandler(_filename, mode="a", encoding="utf-8")
        self.handler.setFormatter(self.formatter)

    def create_logger(self):
        _loger = logging.getLogger(self.log_name)
        _loger.setLevel(getattr(logging, self.level))
        _loger.addHandler(self.handler)
        self.loger = _loger
        return _loger

day = date.today().strftime('%d_%m_%Y')
log = Logger('%s' % day).create_logger()
