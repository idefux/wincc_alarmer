"""
Load and save config.
The config will be json.
"""
import json
import logging


class Config():

    data = None
    filename = None

    def __init__(self, filename=""):
        if filename:
            self.filename = filename
            self.load_config()

    def set_configfile(self, filename):
        self.filename = filename

    def load_config(self):
        """Load config.json and return data object."""
        # logging.info("Loading config.")
        # logging.debug("Looking for config file %s", self.filename)
        with open(self.filename) as config_file:
            self.data = json.load(config_file, encoding="utf-8")

    # def dump_config(self, data):
    #     """Save given data object as config.json."""
    #     logging.info("Saving config.")
    #     filename = "config.json"
    #     logging.debug("Saving config in %s", filename)
    #     with open(filename) as config_file:
    #         json.dump(data, config_file)

    def get_data(self, key):
        """Return data. Load config if not loaded yet."""
        if not self.data:
            self.load_config()
        return self.data[key]

    def get_host(self):
        """Read config and return host."""
        return self.get_data('host')

    def get_database(self):
        """Read config and return database."""
        return self.get_data('database')

    def get_time_interval(self):
        """Read config and return time interval."""
        return self.get_data('time_interval')

    def get_send_email(self):
        """Read config and return send email flag."""
        return self.get_data('send_email')

    def get_send_syslog(self):
        """Read config and return send syslog flag."""
        return self.get_data('send_syslog')

    def get_debug_level(self):
        """Read config and return debug leve."""
        return self.get_data('debug_level')

    def get_syslog_host(self):
        """Read config and return syslog host."""
        return self.get_data('syslog_host')

    def get_syslog_port(self):
        """Read config and return syslog port."""
        return self.get_data('syslog_port')

    def get_syslog_hostname(self):
        """Read config and return hostname (syslog field)."""
        return self.get_data('syslog_hostname')

    def get_syslog_syslogtag(self):
        """Read config and return hostname (syslog field)."""
        return self.get_data('syslog_hostname')

    def get_email_host(self):
        return self.get_data('email_host')

    def get_email_port(self):
        return self.get_data('email_port')

    def get_email_username(self):
        return self.get_data('email_username')

    def get_email_password(self):
        return self.get_data('email_password')

    def get_email_sender(self):
        return self.get_data('email_sender')

    def get_email_receivers(self):
        return self.get_data('email_receivers')

    def get_email_template_path(self):
        return self.get_data('email_template_path')

    def get_email_template_name(self):
        return self.get_data('email_template_name')


config = Config()
