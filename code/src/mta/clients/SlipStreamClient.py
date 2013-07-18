import base64

from slipstream.SlipStreamHttpClient import SlipStreamHttpClient

class SlipStreamClient(SlipStreamHttpClient):
    def __init__(self, configHolder):

        configHolder.set('username',
                         base64.b64decode(configHolder.username))
        configHolder.set('password',
                         base64.b64decode(configHolder.password))

        configHolder.set('cookieFilename', 
                         configHolder.cookie_filename)

        super(SlipStreamClient, self).__init__(configHolder)

        self._check_connection()

    def _check_connection(self):
        self._httpGet(self.serviceRootEndpoint)
        # FIXME: getting user content is more preferable but fails with 401
        # self._getUserContent()