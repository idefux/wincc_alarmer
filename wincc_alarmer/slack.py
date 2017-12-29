from json import dumps
from requests import post

import logging

from wincc_alarmer.config import config
from pywincc.alarm import alarm_state_as_text

slack_webhook_url = None

def read_config():
    global slack_webhook_url
    slack_webhook_url = config.get_slack_webhook_url()


def build_line(alarm):
    return u"{} {} {} {} {} ({})".format(alarm.datetime, alarm.id,
                                         alarm.priority, alarm.location,
                                         alarm.text,
                                         alarm_state_as_text(alarm.state))


def build_data(alarms):
    text = u""
    for alarm in alarms:
        text += build_line(alarm) + u"\n"
    return {"text": text}


def send_alarm_slack(alarms):
    data = build_data(alarms)
    r = post(slack_webhook_url, data=dumps(data))
    logging.info("{} {}".format(r.status_code, r.reason))
