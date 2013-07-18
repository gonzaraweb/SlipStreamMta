
class BaseClient(object):
    def __init__(self, configHolder):
        configHolder.assign(self)
        self.configHolder = configHolder

    def connect(self):
        pass

    def get_messages(self, number_messages=10):
        """Return list of dictionaries, where each dictionary 
        represents a message"""
        raise NotImplementedError()

    def delete_messages(self):
        """If protocol requires explicit deletion of messages 
        implement it here. The method will be invoked after all the consumed 
        message are processed by the client."""
        pass

    def sleep(self):
        """Redefine if queue polling protocol requires timing out. Will 
        be called after messages are read (and removed) from the queue.
        E.g., relevant in case of Amazon SQS."""
        pass
