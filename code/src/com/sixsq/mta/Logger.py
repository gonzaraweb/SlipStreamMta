import os
import errno
import logging

class Logger(object):

    LOGGER_NAME = 'MTA'
    LOGFILE_MAXBYTES = 2*1024*1024
    LOGFILE_BACKUPCOUNT = 5
    LOGFILE_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    log_file = '/var/tmp/slipstream/log/mta.log'

    def __init__(self, configHolder):
        self.log_to_file = True
        configHolder.assign(self)
        self.logger = None
        self._configure_logger()

    def _configure_logger(self):
        self.logger = logging.getLogger(Logger.LOGGER_NAME)

        numeric_level = getattr(logging, self.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % self.log_level)
        self.logger.setLevel(numeric_level)

        formatter = logging.Formatter(self.LOGFILE_FORMAT)

        if self.log_to_file:
            self._create_log_dir()
            handler = logging.handlers.RotatingFileHandler(self.log_file, 
                                           maxBytes=self.LOGFILE_MAXBYTES, 
                                           backupCount=self.LOGFILE_BACKUPCOUNT)
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _create_log_dir(self):
        log_dir = os.path.dirname(self.log_file)
        try:
            os.makedirs(log_dir)
        except OSError, ex:
            if ex.errno != errno.EEXIST:
                raise

    def get_logger(self):
        return self.logger
