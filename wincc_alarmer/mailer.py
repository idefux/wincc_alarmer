from smtplib import SMTP_SSL as SMTP
from smtplib import SMTPException
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from premailer import transform
import logging

from wincc_alarmer.config import config
from pywincc.alarm import AlarmRecord

# Unicode email formatting taken from here:
# http://wordeology.com/computer/how-to-send-good-unicode-email-with-python.html

# Requirements:
# * UTF-8 headers
# * UTF-8 body
# * prefer quoted-printable to base64 transfer-encoding.
# * Don't escape "From" at the beginning of a line in the message - it's not
#   the 1800s any more

from cStringIO import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import Charset
from email.generator import Generator
import os

Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')


class RelEnvironment(Environment):
    """Override join_path() to enable relative template paths."""
    def join_path(self, template, parent):
        return os.path.join(os.path.dirname(parent), template)


def make_email_body(alarms):
    """Use template and alarms object to generate email body."""
    email_template_path = config.get_email_template_path()
    email_template_name = config.get_email_template_name()
    template_vars = {"alarms": alarms,
                     "state_dict": alarms.state_dict,
                     "count": alarms.get_count_grouped()}
    env = Environment(loader=FileSystemLoader(email_template_path))
    # email_template = os.path.join(email_template_path, email_template_name)
    print os.getcwd()
    template = env.get_template(email_template_name)
    # template = env.from_string(EMAIL_BODY_TEMPLATE)
    email_html = template.render(template_vars)
    email_html_out = transform(email_html)
    return email_html_out


def send_alarm_email(alarms):
    """Assemble and build a email for given alarm data."""
    email_host = config.get_email_host()
    email_port = config.get_email_port()
    email_username = config.get_email_username()
    email_password = config.get_email_password()
    email_sender = config.get_email_sender()
    email_receivers = config.get_email_receivers()

    # This example is of an email with text and html alternatives.
    multipart = MIMEMultipart('alternative')

    # We need to use Header objects here instead of just assigning the strings
    # in order to get our headers properly encoded (with QP).
    # You may want to avoid this if your headers are already ASCII, just so
    # people can read the raw message without getting a headache.
    # multipart['To'] = Header(email_receivers.encode('utf-8'), 'UTF-8').encode()
    commaspace = ', '
    multipart['To'] = Header(commaspace.join(email_receivers), 'UTF-8').encode()
    multipart['From'] = Header(email_sender.encode('utf-8'), 'UTF-8').encode()

    alarms_count = alarms.count_come()
    email_subject_prefix = config.get_email_subject_prefix()
    email_subject = email_subject_prefix + u": "
    email_subject += u"%s new alarms" % alarms_count
    multipart['Subject'] = Header(email_subject.encode('utf-8'), 'UTF-8').encode()
    # email_text = email_header_template.format(email_sender=email_sender,
    #                                           email_receivers=email_receivers,
    #                                           email_subject=email_subject)
    html_part = make_email_body(alarms)
    html_part = MIMEText(html_part.encode('utf-8'), 'html', 'UTF-8')
    multipart.attach(html_part)

    text_part = unicode(alarms)
    text_part = MIMEText(text_part.encode('utf-8'), 'plain', 'UTF-8')
    multipart.attach(text_part)
    # email_text = MIMEText(email_text.encode('utf-8'), 'html','utf-8')
    io = StringIO()
    g = Generator(io, False)
    g.flatten(multipart)
    email_text = io.getvalue()

    try:
        smtp_obj = SMTP()
        smtp_obj.connect(email_host, email_port)
        smtp_obj.login(email_username, email_password)
        smtp_obj.sendmail(email_sender, email_receivers, email_text)
        smtp_obj.quit()
        logging.info("Successfully sent email")
    except SMTPException:
        logging.warning("Unable to send email!")


def send_test_email():
    """Send a simple test email to check email service."""
    # Maybe the AlarmRecord() instance can be replaced by an empty list
    # The import would be unnecessary then
    alarms = AlarmRecord()
    send_alarm_email(alarms)
