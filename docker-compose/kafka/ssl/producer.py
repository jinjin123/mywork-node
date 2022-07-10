from kafka import KafkaProducer
import json

class MessageProducer:
    broker = ""
    topic = ""
    username = "admin"
    password = "admin-secret"
    producer = None
    security_protocol = "SASL_PLAINTEXT"
    sasl_mechanism = "PLAIN"
    def __init__(self, broker, topic,security_protocol,sasl_mechanism,username,password ):
        self.broker = broker
        self.topic = topic
        self.security_protocol = security_protocol
        self.sasl_mechanism = sasl_mechanism 
        self.username = username
        self.password = password
        self.producer = KafkaProducer(bootstrap_servers=self.broker,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all',
        retries = 3,
        security_protocol=security_protocol,
        sasl_mechanism=sasl_mechanism,
        sasl_plain_username=username,
         sasl_plain_password=password)


    def send_msg(self, msg):
        print("sending message...")
        try:
            future = self.producer.send(self.topic,msg)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex


broker = 'localhost:9092'
topic = 'test'
username = "admin"
password = "admin-secret"
security_protocol = "SASL_PLAINTEXT"
sasl_mechanism = "PLAIN"
message_producer = MessageProducer(broker,topic,security_protocol, sasl_mechanism,username,password )

data = {'name':'abc', 'email':'abc@example.com'}
resp = message_producer.send_msg(data)
print(resp)
