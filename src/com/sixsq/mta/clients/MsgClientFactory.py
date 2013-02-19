import msg
import msg.AmazonSqsClient as AmazonSqsClient
import msg.DirectoryQueueClient as DirectoryQueueClient

def get_client(configHolder):
    
    if configHolder.msgclient == msg.MSGCLIENT_AMAZON:
        return AmazonSqsClient(configHolder)
    elif configHolder.msgclient == msg.MSGCLIENT_DIRQ:
        return DirectoryQueueClient(configHolder)
    else:
        raise Exception('Unknown messaging client: %s' % configHolder.msgclient)