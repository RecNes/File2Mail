# -*- coding: utf-8 -*-
import sys
from file_ops import GetFileList
from logger import log
from send_by_email import Email

__author__ = 'Sencer Hamarat'


class Main():
    def __init__(self):
        self.email = Email()
        self.email.send(attachments=GetFileList().filtered_list())


def main():
    try:
        Main()
    except Exception as e:
        log.info(e.message)
    finally:
        sys.exit()

if __name__ == "__main__":
    main()
