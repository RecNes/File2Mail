# -*- coding: utf-8 -*-
import ast
import os

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
        """
        Reads settings from file2mail.conf file and applies evaluations to necessary values
        :return: dict()
        """
        try:
            if os.path.isfile(self.file):
                with open(self.file, mode='r') as _file:
                    self.content = _file.readlines()
            else:
                raise Exception(u'Configuration file not found: <<{file}>>'.format(file=self.file))

            try:
                for line in self.content:
                    if (not line.startswith('#')) and ('=' in line):
                        line = line.replace('\r', '').replace('\n', '')
                        key, value = line.split('=')
                        self.config[key.strip()] = value.strip()
            except Exception as e:
                raise Exception(e.message.join(u"Error in configuration file: <<{file}>>".format(file=self.file)))

            if "target_directory" not in self.config or not self.config["target_directory"]:
                raise Exception("Target directory is not specified")

            if "sent_directory" not in self.config or not self.config["sent_directory"]:
                raise Exception("Sent directory is not specified")

            if "sent_directory" not in self.config or not self.config["sent_directory"]:
                self.config["excluded_files"] = []
            elif isinstance(self.config["excluded_files"], str):
                self.config["excluded_files"] = ast.literal_eval(self.config["excluded_files"])

            if "log_level" not in self.config:
                self.config["log_level"] = ''

            if self.config["port"]:
                self.config["port"] = int(self.config["port"])

            self.config["recipients"] = ast.literal_eval(self.config["recipients"])
            return self.config
        except Exception as e:
            raise Exception(e.message)


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SETTINGS = ConfigLoader().read_config()
