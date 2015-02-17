# -*- coding: utf-8 -*-
"""
Application file operations
"""
import os
import shutil
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
            raise Exception("No directory name or path given.")
        self.directory = directory

    @property
    def user_path(self):
        return os.path.expanduser(u"~")

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
        log.debug(u"Checking existence of {directory}".format(directory=self.target_dir_path()))
        return os.path.exists(self.target_dir_path())

    def safe_make_directory(self):
        if not self.check_directory():
            log.warning(u"Directory does not exists: {directory}".format(directory=self.directory))
            if not self.make_directory():
                raise Exception(u"Unable to create directory: {directory}".format(directory=self.directory))
            else:
                log.info(u"Directory created: {directory}".format(directory=self.directory))
        else:
            log.warning(u"Directory exists: {directory}".format(directory=self.directory))


class GetFileList():
    """
    Returns files list in given target directory
    """
    def __init__(self):
        self.fstools = FSTools(SETTINGS["target_directory"])
        self.fstools.safe_make_directory()
        self.target_dir = self.fstools.target_dir_path()
        log.info(u"Getting file list in {target}".format(target=self.target_dir))
        self.file_list = os.listdir(self.target_dir)
        self.file_list = [os.path.join(self.target_dir, f) for f in self.file_list]
        self.exclude_directories()
        self.exclude_files()

    def exclude_directories(self):
        excluded_dirs = list()
        for f in self.file_list:
            if os.path.isdir(f):
                excluded_dirs.append(f)
        log.debug(u"Directories are removed from list: {}".format(repr(excluded_dirs)))
        self.file_list = set(self.file_list).symmetric_difference(excluded_dirs)

    def exclude_files(self):
        excluded_files = list()
        for x in SETTINGS["excluded_files"]:
            for f in self.file_list:
                if f.endswith(x):
                    excluded_files.append(f)
        log.debug(u"Files are removed from list: {}".format(repr(excluded_files)))
        self.file_list = set(self.file_list).symmetric_difference(excluded_files)

    def filtered_list(self):
        if not len(self.file_list):
            raise Exception("There is no file found.")
        log.debug(u"File List Prepared to send : {}".format(self.file_list))
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
        shutil.move(self.source_file, self.target_dir)
        log.debug(u"{file} >> moved to >> {target}".format(file=repr(self.source_file), target=repr(self.target_dir)))
