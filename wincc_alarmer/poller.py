""""
This module polls the wincc server periodically for alarms.
If alarms are found they are sent to the syslog server.
"""
from __future__ import print_function
from datetime import datetime, timedelta
import logging
from time import sleep

from pywincc.wincc import wincc, WinCCException
from pywincc.alarm import alarm_query_builder, AlarmRecord
from wincc_alarmer.mailer import send_alarm_email
from wincc_alarmer.syslog import syslog_message
from wincc_alarmer.config import config


def poll_alarms():
    """Periodically poll the server and syslog found alarms."""
    time_intervall = config.get_time_interval()
    end_time = datetime.now()
    begin_time = end_time - timedelta(seconds=time_intervall)
    host = config.get_host()
    database = config.get_database()
    wincc_instance = wincc(host, database)
    wincc_instance.connect()

    send_email = config.get_send_email()
    send_syslog = config.get_send_syslog()

    alarm_priority = config.get_alarm_priority()
    alarm_priority2 = config.get_alarm_priority2()

    email_priorities = config.get_email_priorities()
    email_states = config.get_email_states()

    syslog_priorities = config.get_syslog_priorities()
    syslog_states = config.get_syslog_states()

    try:
        logging.info("Starting the while loop now.")
        logging.info("You can quit with Ctrl+C or System Exit.")
        while 1:
            try:
                query = alarm_query_builder(begin_time, end_time)
                logging.debug("Built query %s", query)
                wincc_instance.execute(query)
                alarms = wincc_instance.create_alarm_record()
                logging.debug(alarms)
                alarms_count = alarms.count_come()
                logging.info("Found %s new alarms", alarms_count)

                alarms_email = AlarmRecord(alarms.filter_by_priorities(email_priorities))
                alarms_email = alarms_email.filter_by_states(email_states)

                alarms_syslog = AlarmRecord(alarms.filter_by_priorities(syslog_priorities))
                alarms_syslog = alarms_syslog.filter_by_states(syslog_states)

                if send_email and alarms_email:
                    logging.info("Trying to send alarms email.")
                    send_alarm_email(alarms_email)

                if send_syslog and alarms_syslog:
                    logging.info("Trying to send alarms as syslog.")
                    for alarm in alarms_syslog:
                        logging.debug(alarm)
                        syslog_message(alarm)

            except WinCCException as exc:
                print(exc)
            else:
                begin_time = end_time
                logging.info("New begin time %s", begin_time)

            logging.info("Going to sleep now for %s seconds", time_intervall)
            sleep(time_intervall)
            logging.info("I'm back from sleep.")
            end_time = datetime.now()
            logging.debug("New end_time %s", end_time)

    except (KeyboardInterrupt, SystemExit):
        logging.info("Quitting on user request.")
    finally:
        wincc_instance.close()

# if __name__ == "__main__":
#    set_debug_level()
#    poll_alarms()
