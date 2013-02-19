import os
import shutil
import unittest

from dirq.QueueSimple import QueueSimple
from com.sixsq.mta.clients.msg.DirectoryQueueClient import DirectoryQueueClient
from com.sixsq.slipstream.ConfigHolder import ConfigHolder

class DirectoryQueueClientTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.getcwd() + '/test_dir'

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_messages_empty_queue(self):
        QueueSimple(self.test_dir)
        
        qsub = DirectoryQueueClient(ConfigHolder({'msg_queue':self.test_dir},
                                                 config={'foo':'bar'},
                                                 context={'foo':'bar'}))
        qsub.connect()
        assert qsub.get_messages() == []

    def test_get_delete_messages_one(self):
        qpub = QueueSimple(self.test_dir, umask=0)
        qpub.add('message')
        
        qsub = DirectoryQueueClient(ConfigHolder({'msg_queue':self.test_dir},
                                                 config={'foo':'bar'},
                                                 context={'foo':'bar'}))
        qsub.connect()
        assert qsub.get_messages() == ['message']
        assert qpub.count() == 0

    def test_get_delete_messages_max(self):
        num_messages_half = 5
        num_messages_all = 10

        qpub = QueueSimple(self.test_dir)
        for i in range(num_messages_all):
            qpub.add('message %s' % str(i))
        print qpub.count()
        
        qsub = DirectoryQueueClient(ConfigHolder({'msg_queue':self.test_dir},
                                                 config={'foo':'bar'},
                                                 context={'foo':'bar'}))
        qsub.connect()
        assert len(qsub.get_messages(num_messages_half)) == num_messages_half
        assert qpub.count() == num_messages_half
        assert qsub.get_messages(num_messages_half) == ['message %s' % i for i in range(num_messages_half, num_messages_all)]
        assert qpub.count() == 0

if __name__ == "__main__":
    unittest.main()
