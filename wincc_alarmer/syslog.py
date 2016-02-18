"""
Python syslog client.

This code is placed in the public domain by the author.
Written by Christian Stigen Larsen.

This is especially neat for Windows users, who (I think) don't
get any syslog module in the default python installation.

See RFC3164 for more info -- http://tools.ietf.org/html/rfc3164

Note that if you intend to send messages to remote servers, their
syslogd must be started with -r to allow to receive UDP from
the network.
"""

import socket
import logging

from pywincc.alarm import alarm_state_as_text
from pywincc.helper import str_to_datetime, datetime_to_syslog_timestamp
from wincc_alarmer.config import config


FACILITY = {
    'kern': 0, 'user': 1, 'mail': 2, 'daemon': 3,
    'auth': 4, 'syslog': 5, 'lpr': 6, 'news': 7,
    'uucp': 8, 'cron': 9, 'authpriv': 10, 'ftp': 11,
    'local0': 16, 'local1': 17, 'local2': 18, 'local3': 19,
    'local4': 20, 'local5': 21, 'local6': 22, 'local7': 23,
}

LEVEL = {
    'emerg': 0, 'alert': 1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}


def syslog(message, level=LEVEL['notice'], facility=FACILITY['daemon'],
           time='', hostname='', syslogtag='', host='localhost', port=514):
    """
    Send syslog UDP packet to given host and port.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # data = '<%d>%s %s %s' % (level + facility*8, time, hostname, message)
    data = u'<%d>' % (level + facility*8)
    logging.debug(u"syslog time %s", time)
    if time:
        data += u'%s' % time
    if hostname:
        data += u' %s' % hostname
    if syslogtag:
        data += u' %s:' % syslogtag
    data += u'%s' % message
    logging.debug(u"syslog message: %s", data)
    sock.sendto(data.encode('utf-8'), (host, port))
    sock.close()


def syslog_message(alarm):
    """Assemble and send a syslog message for given alarm data."""
    event_time = str_to_datetime(alarm.datetime)
    event_time_syslog = datetime_to_syslog_timestamp(event_time)
    state = alarm_state_as_text(alarm.state)
    syslog_message = unicode(alarm.id) + u': ' + state + u' '
    syslog_message += unicode(alarm.location)
    syslog_message += ' ' + unicode(alarm.text)
    syslog(syslog_message, hostname=config.get_syslog_hostname(),
           syslogtag=config.get_syslog_syslogtag(), time=event_time_syslog,
           host=config.get_syslog_host())
