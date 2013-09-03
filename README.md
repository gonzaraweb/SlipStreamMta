
# Message Tranfer Agent (MTA) 

MTA daemon for consuming/publishing messages. 

Connectors to: pure REST endpoints, [Amazon SQS](http://aws.amazon.com/sqs/) and 
[dirq](https://code.google.com/p/dirq/).

Pluggable and configurable.

Used in [SlipStream](http://sixsq.com/products/slipstream.html) as a consumer of 
messages from Amazon SQS and publisher to specific SlipStream REST resources. 
In particular, consume IDs of the newly built [StratusLab](http://stratuslab.eu/) cloud 
images from SQS and publish them to SlipStream Image module resources.
