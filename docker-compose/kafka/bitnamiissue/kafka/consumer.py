#!/bin/env python
from kafka import KafkaConsumer
 
#connect to Kafka server and pass the topic we want to consume
consumer = KafkaConsumer('test', bootstrap_servers = ['localhost:9092'])
try:
    for msg in consumer:
        print(msg)
        print("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,msg.offset, msg.key, msg.value))
except KeyboardInterrupt as e:
    print(e)
