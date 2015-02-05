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

__author__ = 'Sencer Hamarat'


class Email():
    def __init__(self):
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
        self.sent_attachments = list()

    def __attach_file(self, attachment):
        # Content tipini dosya uzantısından tahmin edeceğiz. Dosyanın Encoding'i görmezden gelinecek
        # fakat dosyanın basit özellikleri kontrol edilecek; Örn: gzip'limi yoksa sıkıştırılmış dosya mı, gibi.
        ctype, encoding = mimetypes.guess_type(attachment)
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
        self.outer.attach(msg)

    def _prepare_email(self, attachment):
        self.outer = MIMEMultipart()
        self.outer['Subject'] = 'You have a new fax {attachment}'.format(attachment=attachment)
        self.outer['To'] = ', '.join(recipient for recipient in self.recipients)
        self.outer['From'] = self.sender

        # TODO: Dosyanın öznitelik bilgileri eklenecek.

        html = """\
        <html>
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
        self.__attach_file(attachment)

    def __prepare_connection(self):
        # If port kwarg is None and tls kwarg is False than self.port is 25
        # If Port kwarg is None and tls kwarg is True than self.port is 587
        # Otherwise self.port is port kwarg
        if self.port is None and self.tls:
            self.port = 587
        elif self.port is None and not self.tls:
            self.port = 25
        else:
            pass

        if not self.host:
            raise Exception("Host not specified")

        if not self.user:
            raise Exception("User is not specified")

        if not self.sender:
            self.sender = self.user

        if not len(self.recipients):
            raise Exception("Recipient(s) not specified")

    def _connection(self, stop=False):
        if not stop:
            self.smtp = smtplib.SMTP()
            self.__prepare_connection()
            self.smtp.connect(self.host, self.port)
            if self.tls:
                self.smtp.starttls()
            self.smtp.login(self.user, self.password)
        else:
            self.smtp.quit()

    def send(self, host=str(), port=None, tls=False, user=str(), password=str(),
             sender=str(), recipients=list(), attachments=list()):

        self.host = host
        self.port = port
        self.tls = tls
        self.user = user
        self.password = password
        self.sender = sender
        self.recipients = recipients
        self.attachments = attachments

        self._connection()

        for attachment in attachments:
            self._prepare_email(attachment)
            self.composed = self.outer.as_string()
            self.smtp.sendmail(self.sender, self.recipients, self.composed)
            self.sent_attachments.append(attachment)

        self._connection(stop=True)
        return self.sent_attachments