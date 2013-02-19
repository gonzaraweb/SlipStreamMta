import time
import base64

from boto.sqs.connection import SQSConnection
from boto.sqs.queue import Queue
from boto.sqs.jsonmessage import JSONMessage
from boto.regioninfo import RegionInfo

from .BaseClient import BaseClient

class AmazonSqsClient(BaseClient):
    
    def __init__(self, configHolder):
        self.log = None
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        super(AmazonSqsClient, self).__init__(configHolder)
        self.amazonsqs_queue_polling_timeout =\
                    float(self.amazonsqs_queue_polling_timeout)
        if not self.aws_access_key_id:
            self.aws_access_key_id = None
        else:
            self.aws_access_key_id = base64.b64decode(self.aws_access_key_id)
        if not self.aws_secret_access_key:
            self.aws_access_key_id = base64.b64decode(self.aws_access_key_id)
        else:
            self.aws_secret_access_key = base64.b64decode(self.aws_secret_access_key)
        self.queue = None
        self.messages = []

    def connect(self):
        region = RegionInfo(name=self.amazonsqs_queue_region,
                            endpoint='eu-west-1.queue.amazonaws.com')
        connection = SQSConnection(region=region,
                                   aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key)
        self.queue = Queue(connection=connection,
                           url=self.amazonsqs_queue_url,
                           message_class=JSONMessage)

    def get_messages(self, number_messages=10):
        self.messages = self.queue.get_messages(num_messages=number_messages)
        self.log.debug("Got %i message(s)." % len(self.messages))
        message_bodies = []
        for m in self.messages:
            message_bodies.append(m.get_body())
        return message_bodies

    def delete_messages(self):
        for m in self.messages[:]:
            self._delete_message(m)
            self.messages.remove(m)

    def _delete_message(self, message):
        if message.queue:
            message.delete()
        else:
            self.queue.delete_message(message)

    def sleep(self):
        time.sleep(self.amazonsqs_queue_polling_timeout)
