# -*- coding: utf-8 -*-
"""
Application file operations
"""
import os
import shutil
import sys
from logger import log
from settings import SETTINGS

__author__ = 'Sencer Hamarat'


class FSTools():
    """
    File System Tools Class
    create_directory: Creates directory in given path
    control_directory: Checks directory existence in given path
    safe_make_directory: Cehcks directory existence before make
    user_path: Returns current user home directory path
    target_dir_path: Returns given target directory full path under current user
    """
    def __init__(self, directory=None):
        if directory is None:
            raise Exception(u"No directory name or path given.")
        self.directory = directory

    @property
    def user_path(self):
        return os.path.expanduser("~")

    def target_dir_path(self):
        return os.path.join(self.user_path, self.directory)

    def make_directory(self):
        created = False
        try:
            os.makedirs(self.target_dir_path())
            created = True
        except Exception as e:
            log.exception(e.message)
        finally:
            return created

    def check_directory(self):
        return os.path.exists(self.target_dir_path())

    def safe_make_directory(self):
        if not self.check_directory():
            if not self.make_directory():
                raise Exception(u"Unable to create directory: <<{directory}>>".format(directory=self.directory))
            else:
                log.info(u"Directory created: <<{directory}>>".format(directory=self.directory))
        else:
            log.warning(u"Directory exsists: <<{directory}>>".format(directory=self.directory))


class GetFileList():
    """
    Returns files list in given target directory
    """
    def __init__(self):
        self.fstools = FSTools(SETTINGS["target_directory"])
        self.target_dir = self.fstools.target_dir_path()
        log.info("Getting file list in {target}".format(target=self.target_dir))
        self.file_list = os.listdir(self.target_dir)
        self.file_list = [os.path.join(self.target_dir, f) for f in self.file_list]
        self.exclude_directories()
        self.exclude_files()

    def exclude_directories(self):
        for f in self.file_list:
            if os.path.isdir(f):
                self.file_list.pop(self.file_list.index(f))

    def exclude_files(self):
        for x in SETTINGS["excluded_files"]:
            for f in self.file_list:
                if f.endswith(x):
                    self.file_list.pop(self.file_list.index(f))

    def filtered_list(self):
        if not len(self.file_list):
            raise Exception("There is no file found.")
        log.info("{count} file{s} found".format(count=len(self.file_list),
                                                s='s' if len(self.file_list) > 1 else ''))
        return self.file_list


class MoveSentFile():
    """
    Moves file in given directory to target directory
    """
    def __init__(self, sent_file=None):
        self.fstools = FSTools(SETTINGS["sent_directory"])
        self.fstools.safe_make_directory()
        self.target_dir = self.fstools.target_dir_path()
        self.source_file = sent_file

    def do(self):
        try:
            shutil.move(self.source_file, self.target_dir)
        except Exception as e:
            raise Exception(e)
        log.info("<<{file}>> moved to <<{target}>>".format(file=self.source_file, target=self.target_dir))