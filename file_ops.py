# -*- coding: utf-8 -*-
import os

__author__ = 'Sencer Hamarat'


class GetFileList():
    def __init__(self, target_folder=None):
        self.target_dir = u"Documents\\Gelen Fax" if target_folder is None else target_folder
        self.excluded_file_types = [".db"]
        self.target_dir_path = os.path.join(self.user_path, self.target_dir)
        self.file_list = os.listdir(self.target_dir_path)
        self.filtered_list = self.exclude_files()

    @property
    def user_path(self):
        return os.path.expanduser("~")

    def exclude_files(self):
        for x in self.excluded_file_types:
            for f in self.file_list:
                if f.endswith(x):
                    self.file_list.pop(self.file_list.index(f))
        return self.file_list





class MoveSentFiles():
    def __init__(self, files_list=None):
        self.sent_files = files_list
        self.gfl = GetFileList()
        self.target_dir_path = os.path.join(self.gfl.user_path, self.gfl.target_dir, u"İletildi")