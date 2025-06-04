# simple_kafka_streaming_pipeline
Creating a simple streaming platform using Apache Kafka
Apache Kafka is a distributed streaming platform used for building data pipelines and event streams. 
## What exactly is streaming data? 
In simple terms streaming data is data flowing continuously from a source. 

## So how does Kafka work then with streaming data
Apache Kafka is a distributed streaming platform that gets continuous information from a source to a target audience. The distributed aspect of the streaming means that Kafka uses a cluster of nodes called Brokers to execute a copy of Apache Kafka. A node is an individual server that processes the data in Apache Kafka.
For streaming data to be chanelled, Kafka uses client based applications to facilitate the streaming called Producers and Consumers. Producers are the source of the data. They take in data organized in messages or virtual groups called Topics and stream the data. Consumers are the client applications that receive the organized information from the Producers.
Therefore, for streaming with Kafka, you need your Topic which is essentially the information you want to stream, producers for writing your topics for streaming and consumers to receive the streamed information.

In this simple demonstration, we will go through the process of setting up and streaming traffic car information which we will then store in a mysql database server. We will use Ubuntu CLI for setting up our Kafka platform and setting up our Mysql server database.

