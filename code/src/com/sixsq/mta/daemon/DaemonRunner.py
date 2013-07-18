import sys

from daemon.runner import is_pidfile_stale
from daemon.runner import DaemonRunner as BaseDaemonRunner

class DaemonRunner(BaseDaemonRunner):

    @staticmethod
    def to_daemonize():
        "daemon.runner.DaemonRunner expects a command line argument."
        return len(sys.argv) >= 2

    def _status(self):
        app_name = self.app.get_app_name()

        pid = self.pidfile.read_pid()

        if not pid:
            print "%s is not running" % app_name
            return

        if is_pidfile_stale(self.pidfile):
            print "%s is not running. Stale PID file %s" % (app_name,
                                                            self.pidfile.path)
        else:
            print "%s (pid %s) is running..." % (app_name, pid)

    action_funcs = dict(BaseDaemonRunner.action_funcs.items() +\
                                            [(u'status', _status)])

    def __init__(self, Runnable):
        """Runnable - subclass from com.sixsq.mta.daemon.DaemonRunnable.DaemonRunnable
        to get required interface."""

        configHolder = Runnable.get_config_holder(
                                    log_to_file=self.to_daemonize())
        try:
            runnable = Runnable(configHolder)
            if self.to_daemonize():
                self.daemonize(runnable)
            else:
                runnable.run()
        except Exception:
            import traceback
            Runnable.get_logger(configHolder).critical(traceback.format_exc())
            raise

    def daemonize(self, runnable):
        super(DaemonRunner, self).__init__(runnable)
        self.daemon_context.files_preserve =\
                            runnable.get_filedescriptors()
        self.do_action()
