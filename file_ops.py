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
        print self.target_dir_path()
        return os.path.exists(self.target_dir_path())

    def safe_make_directory(self):
        if not self.check_directory():
            if not self.make_directory():
                log.error(u"Unable to create directory: <<{directory}>>".format(directory=self.directory))
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
        log.debug(self.file_list)
        self.exclude_directories()
        log.debug(self.file_list)
        self.exclude_files()
        log.debug(self.file_list)
        self.filtered_files = self.file_list

        log.info("{count} file{s} found".format(count=len(self.file_list),
                                                s='s' if len(self.file_list) > 1 else ''))
        sys.exit()

    def exclude_directories(self):
        for f in self.file_list:
            if os.path.isdir(f):
                self.file_list.pop(self.file_list.index(f))

    def exclude_files(self):
        for x in SETTINGS["excluded_files"]:
            for f in self.file_list:
                if f.endswith(x):
                    self.file_list.pop(self.file_list.index(f))


class MoveSentFile():
    """
    Moves file in given directory to target directory
    """
    def __init__(self, files=None):
        self.fstools = FSTools(SETTINGS["sent_directory"])
        self.fstools.safe_make_directory()
        self.target_dir_path = self.fstools.target_dir_path()
        self.source_files = files

    def do(self):
        for source_file in self.source_files:
            try:
                shutil.move(source_file, self.target_dir_path)
            except Exception as e:
                log.error(e)
        log.info("{count} file{s} move to {target}".format(count=len(self.source_files),
                                                           s='s' if len(self.source_files) > 1 else '',
                                                           target=self.target_dir_path))