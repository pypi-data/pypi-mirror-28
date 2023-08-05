#
# Provides function for sending emails from gmail
#
# References:
#  - http://naelshiab.com/tutorial-send-email-python/
#  - https://mail.python.org/pipermail/python-list/2012-November/635909.html
#  - https://stackoverflow.com/questions/26582811/gmail-python-multiple-attachments
#

from contextlib import contextmanager
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import os


max_attachment_size = 10 * (10**6)  # 10 MB


@contextmanager
def gmailsender(fromaddr, passwd):
    """
    Sample usage:

    with gmailsender('<from-address>', '<password>') as mail_sender:
        mail_sender.new_mail('<subject>', ['<to-address>'], ccaddrs=['<cc-address>'])
        mail_sender.set_plain_body('<mail-body>')
        mail_sender.add_attachment('<attachment-1>')
        mail_sender.add_attachment('<attachment-2>')
        mail_sender.send()
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.starttls()
        server.login(fromaddr, passwd)
        yield GMailSenderServer(fromaddr, server)
    except BaseException as e:
        raise e
    finally:
        server.quit()

class GMailSenderServer:
    """
    This class is not responsible for closing an SMTP server, and is not 
    designed to be used directly by user.
    """

    def __init__(self, fromaddr, server):
        self.fromaddr = fromaddr
        self.server = server
        
        # current mail
        self.msg = None        # current email
        self.msg_asize = None  # the total attachment bytes of current mail
        self.toaddrs = None 
        self.ccaddrs = None

    def new_mail(self, subject, toaddrs, ccaddrs=[]):
        """
        Compose a new email. This will overwrite current working email if any.

        :param subject: the single-line non-empty subject string
        :param toaddrs: the non-empty recipient(s) list
        :param ccaddrs: the secondary (Carbon-copy) recipient(s) list
        :return: None
        """
        if subject is None or subject.strip() == '':
            raise ValueError('illegal empty subject')
        if '\n' in subject or '\r' in subject:
            raise ValueError('illegal character "\\n" or "\\r" in subject')
        if toaddrs == []:
            raise ValueError('illegal empty recipient list')
        if len(toaddrs) > len(set(toaddrs)):
            raise ValueError('duplicate recipient(s) in toaddrs')
        if len(ccaddrs) > len(set(ccaddrs)):
            raise ValueError('duplicate recipient(s) in ccaddrs')
        if len(toaddrs) + len(ccaddrs) > len(set(toaddrs + ccaddrs)):
            raise ValueError('overlap recipient(s) in toaddrs and ccaddrs')
        self.msg = MIMEMultipart()
        self.msg['From'] = self.fromaddr
        self.msg['Subject'] = subject
        self.msg['To'] = ', '.join(toaddrs)
        self.msg['Cc'] = ', '.join(ccaddrs)
        
        self.toaddrs = toaddrs
        self.ccaddrs = ccaddrs

    def set_plain_body(self, body):
        """
        Set the body text of an email as plain text. Despite not limited, this 
        method should be called at most once after each call to `new_mail`; 
        otherwise the current email may be corrupted.

        :param body: the body string of current email
        :return: None
        """
        self.msg.attach(MIMEText(body, 'plain'))

    def add_attachment(self, filename, attachment_name=None):
        """
        Add attachment file to current email. If the accumulative bytes of 
        the added attachment(s) plus the size of this attachment exceeds 
        the `max_attachment_size` (10 MB, can be set by modifying this script) 
        for current script setting, ValueError shall be raised.
        
        :param filename: the path of the file to attach
        :param attachment_name: the name shown in email attachment, default
                                to `os.path.basename(filename)`
        :raise ValueError: if the total attachment size exceeds upper limit
        :return: None
        """
        part = MIMEBase('application', 'octet-stream')
        with open(filename, 'rb') as infile:
            content = infile.read()
        total_size = len(content)
        if self.msg_asize is not None:
            total_size += self.msg_asize
        if total_size > max_attachment_size:
            raise ValueError('attachment size exceeds %d bytes'
                    % max_attachment_size)
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(content)
        encoders.encode_base64(part)
        if attachment_name is None:
            attachment_name = os.path.basename(filename)
        part.add_header('Content-Disposition', 
                        'attachment; filename= %s' % attachment_name)
        self.msg.attach(part)

    def send(self):
        """
        Send current email and prepare for a possibly next one. If this 
        method is called before any call to `new_mail`, or if is called 
        more than once after a call to `new_mail`, ValueError shall be 
        raised.

        :raise ValueError: if no email can be sent
        """
        self.server.sendmail(self.fromaddr, 
                        self.toaddrs + self.ccaddrs,
                        self.msg.as_string())
        self.msg = None
        self.msg_asize = None
        self.toaddrs = None
        self.ccaddrs = None
