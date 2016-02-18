from pywincc.alarm import AlarmRecord
from wincc_alarmer.mailer import send_alarm_email
import logging

logging.basicConfig(level=logging.DEBUG)

alarms = AlarmRecord()

send_alarm_email(alarms)
