# -*- coding: utf-8 -*-
import ast
import os
from os.path import isfile

__author__ = 'Sencer Hamarat'


class ConfigLoader():
    """
    Read and parse Configuration file.
    """
    def __init__(self):
        self.content = None
        self.config = dict()
        self.file_name = "file2mail.conf"
        self.file = "{root}/{file}".format(root=PROJECT_ROOT, file=self.file_name)

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
                raise Exception(e.message.join(u"Error in configuration file: <<{file}>>".format(file=self.file)))

            if not hasattr(self.config, "log_level"):
                self.config["log_level"] = ''

            if self.config["port"]:
                self.config["port"] = int(self.config["port"])

            self.config["recipients"] = ast.literal_eval(self.config["recipients"])

            return self.config
        except Exception as e:
            raise Exception(e.message)


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SETTINGS = ConfigLoader().read_config()

