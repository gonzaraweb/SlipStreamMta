import os
import shutil
import unittest
from mock import Mock

from dirq.QueueSimple import QueueSimple
from mta.clients.msg.DirectoryQueueClient import DirectoryQueueClient
from slipstream.ConfigHolder import ConfigHolder

class DirectoryQueueClientTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.getcwd() + '/test_dir'
        shutil.rmtree(self.test_dir, ignore_errors=True)

        self.ch = ConfigHolder({'dirq_queue_location':self.test_dir, 'log' : Mock()}, 
                                config={'foo':'bar'},
                                context={'foo':'bar'})

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_messages_empty_queue(self):
        QueueSimple(self.test_dir)
        
        qsub = DirectoryQueueClient(self.ch)
        qsub.connect()
        assert qsub.get_messages() == []

    def test_get_delete_messages_one(self):
        qpub = QueueSimple(self.test_dir, umask=0)
        qpub.add('123')
        
        qsub = DirectoryQueueClient(self.ch)
        qsub.connect()
        assert qsub.get_messages() == [123]
        assert qpub.count() == 0

    def test_get_delete_messages_max(self):
        num_messages_half = 5
        num_messages_all = 10

        qpub = QueueSimple(self.test_dir)
        for i in range(num_messages_all):
            qpub.add('{"message" : "%i"}' % i)
        
        qsub = DirectoryQueueClient(self.ch)
        qsub.connect()
        messages = qsub.get_messages(num_messages_half)
        assert len(messages) == num_messages_half
        assert qpub.count() == num_messages_half
        messages_read = qsub.get_messages(num_messages_half)
        messages_test = [{'message': str(i)} for i in range(num_messages_half, num_messages_all)]
        assert messages_read == messages_test
        assert qpub.count() == 0

if __name__ == "__main__":
    unittest.main()
