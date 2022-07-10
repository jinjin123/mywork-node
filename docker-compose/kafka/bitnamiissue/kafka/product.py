import time
from kafka import KafkaProducer
 
 
producer = KafkaProducer(bootstrap_servers = ['localhost:9092'])
# Assign a topic
topic = 'test'
 
def test():
    print('begin')
    n = 1
    try:
        while (n<=100):
            producer.send(topic, str(n).encode())
            print("send" + str(n))
            n += 1
            time.sleep(0.5)
    except KafkaError as e:
        print(e)
    finally: 
        producer.close()
        print('done')
 
if __name__ == '__main__':
    test()
