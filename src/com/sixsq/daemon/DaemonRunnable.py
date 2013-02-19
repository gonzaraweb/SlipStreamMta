import os
import sys

class DaemonRunnable(object):
    def __init__(self, configHolder):
        self.pidfile_path = '/tmp/daemonrunnable.pid'

        configHolder.assign(self)
        self.configHolder = configHolder

        # For DaemonRunner
        self.stdin_path = '/dev/null'
        self.stdout_path = self.log_file + '.stdout'
        self.stderr_path = self.log_file + '.stderr'
        self.pidfile_timeout = 3

    def run(self):
        raise NotImplementedError()
    
    def get_logger(self):
        raise NotImplementedError()

    def get_config_holder(self):
        raise NotImplementedError()

    def get_filedescriptors(self):
        "Provide a list of file descriptors not to be touched by DaemonRunner."
        return self._get_logger_filedescriptors()

    def _get_logger_filedescriptors(self):
        fds = []
        for h in self.log.handlers:
            try:
                fds.append(h.stream.fileno())
            except:
                pass
        return fds

    def get_app_name(self):
        return os.path.basename(sys.argv[0])
