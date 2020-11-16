import logging
import logging.config
import yaml


with open("log/log_config.yml", "r") as f:
    log_cfg = yaml.safe_load(f.read())

logging.config.dictConfig(log_cfg)


def get_logger(name):
    return WhorkovLogger(name)


class WhorkovLogger:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
