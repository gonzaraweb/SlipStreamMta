import os
import sys

from slipstream.ConfigHolder import ConfigHolder

from mta.daemon import DaemonRunnable

from .Logger import Logger
from .clients import MsgClientFactory
from .clients import SlipStreamClient

CONF_FILES = ['/etc/slipstream/mta.cfg', 
              os.path.dirname(sys.argv[0]) + '/../etc/mta.cfg']
def _get_conf_file():
    for cf in CONF_FILES:
        if os.path.exists(cf):
            return cf

class MTA(DaemonRunnable):
    "Message Transfer Agent"

    REQUIRED_MESSAGE_ATTRIBUTES = ['uri', 'imageid']

    config_file = _get_conf_file()
    
    @staticmethod
    def get_logger(configHolder):
        return configHolder.options.get('log') or \
                    Logger(configHolder).get_logger()
    
    @staticmethod
    def get_config_holder(log_to_file=True):
        configHolder = ConfigHolder(context={'empty':None}, 
                                    configFile=MTA.config_file)

        configHolder.set('log_to_file', log_to_file)
        configHolder.set('log', MTA.get_logger(configHolder))
        
        return configHolder
    
    def __init__(self, configHolder):
        super(MTA, self).__init__(configHolder)

        self.msg = None
        self.ss = None

    def _init_MsgClient(self):
        self.msg = MsgClientFactory.get_client(self.configHolder)
        self.msg.connect()

    def _init_SlipStreamClient(self):
        self.ss = SlipStreamClient(configHolder=self.configHolder)
        
    def _init_clients(self):
        self.log.info("MTA starting.")
        self.log.debug(self.configHolder)

        self._init_MsgClient()
        self._init_SlipStreamClient()

    def run(self):

        self._init_clients()

        while True:
            messages = self.msg.get_messages()
            if messages:
                for body in messages:
                    self.log.debug("Got message: %s", str(body))

                    if not self._message_body_valid(body):
                        continue

                    try:
                        self.ss.putNewImageId(body['uri'], body['imageid'])
                    except Exception, ex:
                        self.log.critical("Failed to put new image ID with: %s",
                                          str(ex))
                self.msg.delete_messages()

            self.msg.sleep()
            
    def _message_body_valid(self, body):
        if not isinstance(body, dict) or \
            (not body.has_key('uri') or not body.has_key('imageid')):
            self.log.warning('Bad message body for publishing. Expected dict with keys %s' %\
                             str(self.REQUIRED_MESSAGE_ATTRIBUTES))
            return False
        return True

        
        