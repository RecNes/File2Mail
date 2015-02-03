# -*- coding: utf-8 -*-
import os
from os.path import isfile
from logger import log

__author__ = 'Sencer Hamarat'


class ConfigLoader():
    """
    Reading Configuration file.
    """
    def __init__(self):
        self.content = None
        self.content_dict = dict()
        self.file_name = "file2mail.conf"
        self.file = "{root}/{file}".format(root=Settings.PROJECT_ROOT, file=self.file_name)

    def read_config(self):
        try:
            if isfile(self.file):
                with open(self.file, mode='r') as _file:
                    self.content = _file.readlines()
            else:
                hata = u'Configuration file not found: <<{file}>>'.format(file=self.file)
                log.error(hata)
            try:
                for line in self.content:
                    if (not line.startswith('#')) and ('=' in line):
                        line = line.replace('\r', '').replace('\n', '').replace(' ', '')
                        key, value = line.split('=')
                        self.content_dict[key] = value
            except Exception as e:
                log.exception(e.message)
                log.error(u"Error in configuration file: <<{file}>>".format(file=self.file))
                raise Exception(u"ERROR: Configuration error...")

            return self.content

        except Exception as e:
            log.exception(e.message)


class Settings():
    def __init__(self):
        pass

    DEBUG = False
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


