# -*- coding: utf-8 -*-
import ast
from file_ops import GetFileList, MoveSentFile
from logger import log
from send_by_email import Email
from settings import SETTINGS


__author__ = 'Sencer Hamarat'


class Main():
    def __init__(self):
        self.email = Email()
        if SETTINGS["port"]:
            self.port = int(SETTINGS["port"])
        else:
            self.port = SETTINGS["port"]
        self.recipients = ast.literal_eval(SETTINGS["recipients"])

    def start_and_run(self):
        file_list = GetFileList().full_file_list

        if len(file_list):
            sent_files = self.email.send(host=SETTINGS["host"], port=self.port, tls=SETTINGS["tls"],
                                         user=SETTINGS["user"], password=SETTINGS["password"],
                                         sender=SETTINGS["sender"], recipients=self.recipients,
                                         attachments=file_list)
        else:
            raise Exception("There is no file found.")

        if len(sent_files):
            move_files = MoveSentFile(target_dir=None, files=sent_files)
            move_files.do()
        else:
            raise Exception("No files were moved")


def main():
    try:
        Main().start_and_run()
    except Exception as e:
        log.exception(e.message)
    finally:
        exit()

if __name__ == "__main__":
    main()
