"""
Load and save config.
The config will be json.
"""
import json


class Config(object):
    """This class holds the global config for the wincc_alarmer."""

    data = None
    filename = None

    def __init__(self, filename=""):
        if filename:
            self.filename = filename
            self.load_config()

    def set_configfile(self, filename):
        """Set filename (path) of config file."""
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
        """Read config and return debug level."""
        return self.get_data('debug_level')

    def get_syslog_host(self):
        """Read config and return syslog host."""
        return self.get_data('syslog_host')

    def get_syslog_port(self):
        """Read config and return syslog port."""
        return self.get_data('syslog_port')

    def get_syslog_use_tls(self):
        """Read config and return syslog use tls flag."""
        return self.get_data('syslog_use_tls')

    def get_syslog_tls_port(self):
        """Read config and return syslog tls port."""
        return self.get_data('syslog_tls_port')

    def get_syslog_tls_cert(self):
        """Read config and return syslog tls certificate."""
        return self.get_data('syslog_tls_cert')

    def get_syslog_hostname(self):
        """Read config and return hostname (syslog field)."""
        return self.get_data('syslog_hostname')

    def get_syslog_syslogtag(self):
        """Read config and return hostname (syslog field)."""
        return self.get_data('syslog_hostname')

    def get_email_host(self):
        """Read config and return hostname of email service."""
        return self.get_data('email_host')

    def get_email_port(self):
        """Read config and return port number of email service."""
        return self.get_data('email_port')

    def get_email_username(self):
        """Read config and return username for of email service login."""
        return self.get_data('email_username')

    def get_email_password(self):
        """Read config and return password for of email service login."""
        return self.get_data('email_password')

    def get_email_sender(self):
        """Read config and return sender name for email."""
        return self.get_data('email_sender')

    def get_email_receivers(self):
        """Read config and return a list of email receivers."""
        return self.get_data('email_receivers')

    def get_email_subject_prefix(self):
        """Read config and return prefix for email subject."""
        return self.get_data('email_subject_prefix')

    def get_email_template_path(self):
        """Read config and return the emails template path."""
        return self.get_data('email_template_path')

    def get_email_template_name(self):
        """Read config and return filename for the email template."""
        return self.get_data('email_template_name')

    def get_syslog_priorities(self):
        """Read config and return a list of priorities to pass filter."""
        return self.get_data('syslog_priorities')

    def get_syslog_states(self):
        """Read config and return a list of states to pass filter."""
        return self.get_data('syslog_states')

    def get_email_priorities(self):
        """Read config and return a list of priorities to pass filter."""
        return self.get_data('email_priorities')

    def get_email_states(self):
        """Read config and return a list of states to pass filter."""
        return self.get_data('email_states')

    def get_send_slack(self):
        """Read config and return send slack flag."""
        return self.get_data('send_slack')

    def get_slack_webhook_url(self):
        """Read config and return the url for the slack webhook."""
        return self.get_data('slack_webhook_url')

    def get_slack_priorities(self):
        """Read config and return a list of priorities to pass filter."""
        return self.get_data('slack_priorities')

    def get_slack_states(self):
        """Read config and return a list of states to pass filter."""
        return self.get_data('slack_states')

config = Config()
