from json import dumps
from requests import post

import logging

from wincc_alarmer.config import config
from pywincc.alarm import alarm_state_as_text

zulip_webhook_url = None
zulip_base_url = None
zulip_stream = None
zulip_topic = None
zulip_api_key = None

def read_config():
    global zulip_webhook_url
    global zulip_base_url
    global zulip_stream
    global zulip_topic
    global zulip_api_key
    zulip_base_url = config.get_zulip_base_url()
    zulip_stream = config.get_zulip_stream()
    zulip_topic = config.get_zulip_topic()
    zulip_api_key = config.get_zulip_api_key()
    zulip_webhook_url = "{}?api_key={}&stream={}".format(zulip_base_url,
                                                         zulip_api_key,
                                                         zulip_stream)


def build_line(alarm):
    return u"{} {} {} {} {} ({})".format(alarm.datetime, alarm.id,
                                         alarm.priority, alarm.location,
                                         alarm.text,
                                         alarm_state_as_text(alarm.state))


def build_data(alarms, topic):
    text = u""
    for alarm in alarms:
        text += build_line(alarm) + u"\n"
    return {"text": text, "topic": topic}


def send_alarm_zulip(alarms):
    data = build_data(alarms, zulip_topic)
    r = post(zulip_webhook_url, data=dumps(data))
    logging.info("{} {}".format(r.status_code, r.reason))
