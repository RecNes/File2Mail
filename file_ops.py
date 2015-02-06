# -*- coding: utf-8 -*-
"""
Application file operations
"""
import os
import shutil
from logger import log

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
    def __init__(self, target_dir=None, exclude=None):
        self.excluded_file_types = [".db"] if exclude is None else exclude
        self.target_dir = u"Documents\\Gelen Fax" if target_dir is None else target_dir
        self.fstools = FSTools(self.target_dir)
        self.target_dir_path = self.fstools.target_dir_path()
        log.info("Getting file list in {target}".format(target=self.target_dir_path))
        self.file_list = os.listdir(self.target_dir_path)
        self.filtered_list = self.exclude_files()
        self.full_file_list = [os.path.join(self.target_dir_path, f) for f in self.filtered_list]
        log.info("{count} file{s} found".format(count=len(self.full_file_list),
                                                s='s' if len(self.full_file_list) > 1 else ''))

    def exclude_files(self):
        for x in self.excluded_file_types:
            for f in self.file_list:
                if f.endswith(x):
                    self.file_list.pop(self.file_list.index(f))
        return self.file_list


class MoveSentFile():
    """
    Moves file in given directory to target directory
    """
    def __init__(self, target_dir=None, files=None):
        self.target_dir = u"Documents\\Gelen Fax\\İletildi" if target_dir is None else target_dir
        self.fstools = FSTools(self.target_dir)
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