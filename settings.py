# -*- coding: utf-8 -*-
import os
from os.path import isfile
from logger import log

__author__ = 'Sencer Hamarat'


class ConfigLoader():
    """
    Read and parse Configuration file.
    """
    def __init__(self):
        self.content = None
        self.config = dict()
        self.file_name = "file2mail.conf"
        self.file = "{root}/{file}".format(root=Settings.PROJECT_ROOT, file=self.file_name)

    def read_config(self):
        try:
            if isfile(self.file):
                with open(self.file, mode='r') as _file:
                    self.content = _file.readlines()
            else:
                raise Exception(u'Configuration file not found: <<{file}>>'.format(file=self.file))

            try:
                for line in self.content:
                    if (not line.startswith('#')) and ('=' in line):
                        line = line.replace('\r', '').replace('\n', '').replace(' ', '')
                        key, value = line.split('=')
                        self.config[key] = value
            except Exception as e:
                log.exception(e.message)
                raise Exception(u"Error in configuration file: <<{file}>>".format(file=self.file))

            return self.config

        except Exception as e:
            log.exception(e.message)


class Settings():
    def __init__(self):
        self.settings = ConfigLoader().read_config()
        if not "DEBUG" in self.settings:
            self.settings["DEBUG"] = False

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SETTINGS = __init__().settings

