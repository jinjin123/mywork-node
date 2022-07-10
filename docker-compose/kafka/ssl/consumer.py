from kafka import KafkaConsumer, consumer
from time import sleep
import json


class MessageConsumer:
    broker = ""
    topic = ""
    group_id = ""
    logger = None
    username = "admin"
    password = "admin-secret"
    security_protocol = "SASL_PLAINTEXT"
    sasl_mechanism = "PLAIN"
    def __init__(self, broker, topic,group_id,security_protocol,sasl_mechanism,username,password ):
        self.broker = broker
        self.topic = topic
        self.group_id = group_id
        self.security_protocol = security_protocol
        self.sasl_mechanism = sasl_mechanism 
        self.username = username
        self.password = password
    def activate_listener(self):
        consumer = KafkaConsumer(bootstrap_servers=self.broker,
                                 group_id='my-group',
                                 consumer_timeout_ms=60000,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 security_protocol=security_protocol,
                                 sasl_mechanism=sasl_mechanism,
                                 sasl_plain_username=username,
                                  sasl_plain_password=password)
                                 #value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        consumer.subscribe(self.topic)
        print("consumer is listening....")
        try:
            for message in consumer:
                print("received message = ", message)

                #committing message manually after reading from the topic
                consumer.commit()
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()


#Running multiple consumers
broker = 'localhost:9092'
topic = 'test'
group_id = 'consumer-1'
username = "admin"
password = "admin-secret"
security_protocol = "SASL_PLAINTEXT"
sasl_mechanism = "PLAIN"
consumer1 = MessageConsumer(broker,topic,group_id,security_protocol, sasl_mechanism,username,password )
consumer1.activate_listener()

consumer2 = MessageConsumer(broker,topic,group_id,security_protocol, sasl_mechanism,username,password )
consumer2.activate_listener()
