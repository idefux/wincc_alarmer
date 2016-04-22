"""
Send syslog message for test purposes
"""
from pywincc.alarm import Alarm
from wincc_alarmer.config import config
from wincc_alarmer.syslog import syslog_message
from pywincc.helper import datetime_to_str
from datetime import datetime
import logging


config.set_configfile("..\config.json")
config.load_config()
logging.basicConfig(level=logging.DEBUG)

test_alarm = Alarm('1234', '2', datetime_to_str(datetime.now()), 'CLASSNAME',
                   'TEST_ERROR', 'Office', 'This is a test syslog message')

syslog_message(test_alarm)
