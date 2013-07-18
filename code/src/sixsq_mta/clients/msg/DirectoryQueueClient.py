import time
import json

from .BaseClient import BaseClient
from dirq.QueueSimple import QueueSimple

TIME_GRANULARITY = 3600 # sec

class DirqJsonMessages(QueueSimple):
    def __init__(self, path, umask, granularity):
        super(DirqJsonMessages, self).__init__(path, umask, granularity)
    def get(self, name):
        message = super(DirqJsonMessages, self).get(name)
        return json.loads(message)

class DirectoryQueueClient(BaseClient):
    def __init__(self, configHolder):
        self.log = None
        self.dirq_queue_umask = 0
        self.dirq_queue_polling_timeout = 60
        super(DirectoryQueueClient, self).__init__(configHolder)
        self.dirq_queue_umask = int(self.dirq_queue_umask)
        self.dirq_queue_polling_timeout = float(self.dirq_queue_polling_timeout)
        self.queue = None

    def connect(self):
        self.queue = DirqJsonMessages(self.dirq_queue_location,
                                             self.dirq_queue_umask,
                                             granularity=TIME_GRANULARITY)

    def get_messages(self, number_messages=10):
        message_bodies = []
        i = 0
        for name in self.queue:
            if not self.queue.lock(name):
                continue
            self.log.info("Got message id '%s' to process" % name)
            try:
                message = self.queue.get(name)
            except ValueError, e:
                self.log.warning("Failed to get message '%s' with '%s'" % (name, str(e)))
                # TODO: move the messages to dead letter queue.
                continue
            message_bodies.append(message)
            self.queue.remove(name)
            i += 1
            if i >= number_messages:
                break
        return message_bodies

    def sleep(self):
        time.sleep(self.dirq_queue_polling_timeout)
