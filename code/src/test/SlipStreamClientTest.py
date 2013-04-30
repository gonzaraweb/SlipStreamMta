import unittest

import base64
import shutil 
import os

from com.sixsq.mta.clients.SlipStreamClient import SlipStreamClient
from com.sixsq.slipstream.ConfigHolder import ConfigHolder

class SlipStreamClientTest(unittest.TestCase):
    
    def tearDown(self):
        shutil.rmtree('%s/.cache/' % os.getcwd(), ignore_errors=True)
    
    def test_init(self):
        ssc = SlipStreamClient(ConfigHolder({'username':base64.b64encode('user'), 
                                             'password':base64.b64encode('pass'), 
                                             'cookie_filename':'cookies'},
                                             context={'foo':'bar'},
                                             config={'foo':'bar'}))
        assert ssc.username == 'user'
        assert ssc.password == 'pass'
        assert ssc.cookieFilename == 'cookies'

if __name__ == "__main__":
    unittest.main()