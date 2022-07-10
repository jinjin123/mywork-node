#!/bin/env python
from pykafka import KafkaClient
host = 'localhost:9092'
client = KafkaClient(hosts = host)
topic = client.topics["test".encode()]
# 将产生kafka同步消息，这个调用仅仅在我们已经确认消息已经发送到集群之后
with topic.get_sync_producer() as producer:
    for i in range(100):
        producer.produce(('test message ' + str(i ** 2)).encode())
