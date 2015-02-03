# -*- coding: utf-8 -*-
import os
import smtplib
import mimetypes
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from file_ops import GetFileList

__author__ = 'Sencer Hamarat'


class Email():
    def __init__(self, recipients=None, host=None, port=None, tls=None, user=None, password=None,):
        self.COMMASPACE = ', '
        self.composed = None
        self.outer = None
        self.get_file_list = GetFileList()
        self.host = 'mail.yapifizigi.com' if host is None else host
        self.port = 587 if port is None else port
        self.tls = True if tls is None else tls
        self.smtp_user = '' if user is None else user
        self.smtp_pass = '' if password is None else password
        self.sender = 'fax@yapifizigi.com'
        self.dir = self.get_file_list.target_dir_path
        self.recipients = ['sencerhamarat@gmail.com'] if recipients is None else recipients
        self.file_list = self.get_file_list.filtered_list
        self.ready_to_move = []

    def attach_file(self, filename):
        path = os.path.join(self.dir, filename)
        # if not os.path.isfile(path):
        #     continue

        # Content tipini dosya uzantısından tahmin edeceğiz. Dosyanın Encoding'i görmezden gelinecek
        # fakat dosyanın basit özellikleri kontrol edilecek; Örn: gzip'limi yoksa sıkıştırılmış dosya mı, gibi.
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open(path)
            # Not: charset hesaplamasını yapmalıyız.
            msg = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            fp.close()
            # Base64 Encoding kullanarak yükleme
            encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        self.outer.attach(msg)

    def prepare_email(self, filename):
        self.outer = MIMEMultipart()
        self.outer['Subject'] = 'Yeni bir faksınız var {0}'.format(filename)
        self.outer['To'] = self.COMMASPACE.join(recipient for recipient in self.recipients)
        self.outer['From'] = self.sender

        # TODO: Dosyanın öznitelik bilgileri eklenecek.

        html = """\
        <html>
            <head></head>
            <body>
                <p>
                    Merhaba!
                </p>
                <p>
                    Yeni bir faks alındı: {0}.<br>
                    Gelen faksı görmek için lütfen bu e-postanın ekindeki dosyaya bakınız.
                </p>
                <p style="float: right;">
                    File2Mail by Sencer Hamarat (C) 2015
                </p>
            </body>
        </html>
        """.format(filename,)
        self.outer.attach(MIMEText(html, 'html'))
        self.outer.preamble = filename
        self.attach_file(filename)

    def send(self):
        s = smtplib.SMTP()
        s.connect(self.host, self.port)
        s.starttls()
        s.login(self.smtp_user, self.smtp_pass)
        for filename in self.file_list:
            self.prepare_email(filename)
            self.composed = self.outer.as_string()
            s.sendmail(self.sender, self.recipients, self.composed)
            self.ready_to_move.append(filename)
        s.quit()
        return self.ready_to_move