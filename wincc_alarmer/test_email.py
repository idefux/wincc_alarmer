from pywincc.alarm import AlarmRecord
from wincc_alarmer.mailer import send_alarm_email
from wincc_alarmer.config import config
import logging


config.set_configfile("..\config.json")
config.load_config()
logging.basicConfig(level=logging.DEBUG)
alarms = AlarmRecord()
send_alarm_email(alarms)
