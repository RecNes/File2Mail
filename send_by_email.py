# -*- coding: utf-8 -*-
"""
Prepare and send files as attachment by e-mail
"""
import smtplib
import mimetypes
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from file_ops import MoveSentFile
from logger import log
from settings import SETTINGS

__author__ = 'Sencer Hamarat'


class Email():
    def __init__(self):
        log.debug("Email Class initiated")
        self.host = str()
        self.port = int()
        self.tls = False
        self.user = str()
        self.password = str()
        self.sender = str()
        self.recipients = list()
        self.composed = str()
        self.outer = None
        self.attachments = list()
        self.smtp = None

    def __attach_file(self, attachment):
        """
        Guess content type of the attachment, prepare header with this knowledge and attach file to message
        :param attachment:
        :return: None
        """
        log.debug("{attachment} file prepairing to attach...".format(attachment=attachment))
        ctype, encoding = mimetypes.guess_type(attachment)
        log.debug("File type and encoding is: {ctype} / {encoding}".format(ctype=ctype, encoding=encoding))
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open(attachment)
            # Not: charset hesaplamasını yapmalıyız.
            msg = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(attachment, 'rb')
            msg = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(attachment, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(attachment, 'rb')
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            fp.close()
            # Base64 Encoding kullanarak yükleme
            encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=attachment)
        log.debug("File attached to message.")
        self.outer.attach(msg)

    def _prepare_email(self, attachment):
        """
        Prepare e-mail body and append attachments
        """
        log.debug("Mail prepairing to send...")
        self.outer = MIMEMultipart()
        self.outer['Subject'] = 'You have a new fax {attachment}'.format(attachment=attachment)
        self.outer['To'] = ', '.join(recipient for recipient in self.recipients)
        self.outer['From'] = self.sender

        # TODO: Dosyanın öznitelik bilgileri eklenecek.

        html = """<html>
            <head></head>
            <body>
                <p>
                    Hello!
                </p>
                <p>
                    You have a new fax: {attachment}.<br>
                    Please take a look at the attachment in this e-mail to see received fax.
                </p>
                <p style="float: right;">
                    File2Mail by Sencer Hamarat (C) 2015
                </p>
            </body>
        </html>
        """.format(attachment=attachment)
        self.outer.attach(MIMEText(html, 'html'))
        self.outer.preamble = attachment
        log.debug("Message added to mail.")
        self.__attach_file(attachment)

    def __prepare_connection(self):
        """
        Check and prepare connection variables with given kwargs
        :return:
        """
        # If port kwarg is None and tls kwarg is False than self.port is 25
        # If Port kwarg is None and tls kwarg is True than self.port is 587
        # Otherwise self.port is port kwarg
        if self.tls and not self.port:
            self.port = 587
        elif not self.port and not self.tls:
            self.port = 25
        else:
            pass
        log.debug("Port setted to {port}".format(port=self.port))

        if not self.host:
            raise Exception("Host not specified")

        if not self.user:
            raise Exception("User is not specified")

        if not self.sender:
            self.sender = self.user

        if not len(self.recipients):
            raise Exception("Recipient(s) not specified")

    def _connection(self, stop=False):
        """
        If stop kwarg True then start connection else stop connection
        :param stop: bool
        :return: None
        """
        if not stop:
            log.info("Connecting to <<{host}>> host...".format(host=self.host))
            self.smtp = smtplib.SMTP()
            self.__prepare_connection()
            self.smtp.connect(self.host, self.port)
            log.info("Connected to <<{host}>> host".format(host=self.host))

            if self.tls:
                log.info("Starting TLS...")
                self.smtp.starttls()
                log.info("TLS Started.")
            log.info("Logging in with user credentials...")
            self.smtp.login(self.user, self.password)
            log.info("Logged in.")
        else:
            self.smtp.quit()
            log.info("Connection to <<{host}>> is now closed.".format(host=self.host))

    def send(self, attachments=list()):
        """
        Make SMTP connection and send mail per attachments and return sent attachments list
        :param attachments:
        :return: list()
        """
        self.host = SETTINGS["host"]
        self.port = SETTINGS["port"]
        self.tls = SETTINGS["tls"]
        self.user = SETTINGS["user"]
        self.password = SETTINGS["password"]
        self.sender = SETTINGS["sender"]
        self.recipients = SETTINGS["recipients"]

        self.attachments = attachments
        self._connection()

        for attachment in attachments:
            self._prepare_email(attachment)
            self.composed = self.outer.as_string()
            log.debug("{file} is now sending".format(file=attachment))
            self.smtp.sendmail(self.sender, self.recipients, self.composed)
            log.info("{file} is sent".format(file=attachment))
            MoveSentFile(sent_file=attachment).do()

        self._connection(stop=True)