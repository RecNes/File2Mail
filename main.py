# -*- coding: utf-8 -*-
from file_ops import MoveSentFiles
from send_by_email import Email

__author__ = 'Sencer Hamarat'


def main():
    email = Email()
    sent_files = email.send()
    if len(sent_files):
        MoveSentFiles(sent_files)
    exit()

if __name__ == "__main__":
    main()
