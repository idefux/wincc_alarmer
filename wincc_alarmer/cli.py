"""
This is the command line interface for the wincc_alarmer.
Currently you can only hand in the configuration file here.
"""

import click
import logging

from wincc_alarmer.poller import poll_alarms
from wincc_alarmer.config import config
from wincc_alarmer.mailer import send_test_email


def set_debug_level():
    """Set debug level for this module."""
    debug_level = config.get_debug_level()
    if debug_level >= 2:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Set logging level to DEBUG.")
    elif debug_level == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


def set_config(config_file):
    """Set global config."""
    config.set_configfile(config_file)
    config.load_config()


@click.command()
@click.argument('config_file')
def poll(config_file):
    """Main entry point. Loads config file and calls poll function."""
    set_config(config_file)
    set_debug_level()
    poll_alarms()


@click.command()
@click.argument('config_file')
def test_email(config_file):
    """Simple routine for sending a test email."""
    set_config(config_file)
    set_debug_level()
    send_test_email()
