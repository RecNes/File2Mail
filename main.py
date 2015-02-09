# -*- coding: utf-8 -*-
import sys
from file_ops import GetFileList, MoveSentFile
from logger import log
from send_by_email import Email
from settings import SETTINGS


__author__ = 'Sencer Hamarat'


class Main():
    def __init__(self):
        self.email = Email()

    def start_and_run(self):
        file_list = GetFileList().filtered_files

        if len(file_list):
            sent_files = self.email.send(attachments=file_list)
        else:
            raise Exception("There is no file found.")

        if len(sent_files):
            move_files = MoveSentFile(files=sent_files)
            move_files.do()
        else:
            raise Exception("No files were moved")


def main():
    try:
        Main().start_and_run()
    except Exception as e:
        log.exception(e.message)
    finally:
        sys.exit()

if __name__ == "__main__":
    main()
