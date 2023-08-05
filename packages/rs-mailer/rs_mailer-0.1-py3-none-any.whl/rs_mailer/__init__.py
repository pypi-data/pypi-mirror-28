__all__ = ['EmailSender']

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import os


class EmailSender():

    def __init__(self, id, password, smtp_address, port_number, ssl_needed,
                 recipient_addresses,
                 subject, msg_body, cc_addresses=None, attachments_path=None, 
                 smtplib_debug=False):
        # Login information for SMTP Server
        self.id = id
        self.password = password
        self.smtp_address = smtp_address
        self.port_number = port_number
        self.ssl_needed = ssl_needed
        self.smtplib_debug = smtplib_debug

        # Create the message
        self.msg = MIMEMultipart()

        # Recipient of the message
        self.recipient_addresses = recipient_addresses

        if type(self.recipient_addresses) == list:
            self.msg['To'] = ", ".join(self.recipient_addresses)
        else:
            self.msg['To'] = self.recipient_addresses

        self.msg['From'] = self.id
        self.msg['Subject'] = subject

        if cc_addresses is not None:
            self.cc_addresses = cc_addresses
            if type(self.cc_addresses) == list:
                self.msg['cc'] = ", ".join(self.cc_address)
            else:
                self.msg['cc'] = self.cc_addresses
        else:
            self.cc_addresses = ''

        # Attach the text of the body
        self.msg.attach(MIMEText(msg_body.encode('utf-8'), _charset='utf-8'))

        # Attach files
        if attachments_path != None:
            if type(attachments_path) == list:
                for file_path in attachments_path:
                    part = process_attachment_file(file_path)
                    self.msg.attach(part)
            else:
                part = process_attachment_file(attachments_path)
                self.msg.attach(part)

    def send(self):
        if type(self.recipient_addresses) == list:
            if type(self.cc_addresses) == list:
                all_recipients_list = self.recipient_addresses + self.cc_addresses
            else:
                all_recipients_list = self.recipient_addresses
                all_recipients_list.append(self.cc_addresses)
        else:
            all_recipients_list = []
            all_recipients_list.append(self.recipient_addresses)
            all_recipients_list.append(self.cc_addresses)

        if self.ssl_needed:
            smtp_server = smtplib.SMTP_SSL(self.smtp_address, self.port_number)
        else:
            smtp_server = smtplib.SMTP(self.smtp_address, self.port_number)

        if self.smtplib_debug:
            smtp_server.set_debuglevel(True)

        smtp_server.login(self.id, self.password)

        smtp_server.sendmail(
            self.id,
            all_recipients_list,
            self.msg.as_string()
        )
        smtp_server.close()


def process_attachment_file(file_path):

    # Files need to be read in binary mode to be encoded in base64
    file_object = open(file_path, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((file_object).read())
    encoders.encode_base64(part)

    file_name = os.path.basename(file_object.name)

    part.add_header(
        'Content-Disposition',
        "attachment; filename= %s" % (Header(file_name, 'utf-8').encode())
    )

    return part
