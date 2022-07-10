class KafkaConsumer(object):
    def __init__(self, hosts, topic):
        self.client = KafkaClient(hosts=hosts)
        self.topic = self.client.topics[topic.encode()]
    def simple_consumer(self, offset=0):
        """
        指定消费
        :param offset:
        :return:
        """
        partitions = self.topic.partitions
        print("分区：", partitions)
        print("last_offset", self.topic.latest_available_offsets())
        # 自动提交消费
        consumer = self.topic.get_simple_consumer(b"simple_consumer",
                                                  partitions=[partitions[1]], auto_commit_enable=True,auto_commit_interval_ms=1)
        # for i in range(100):
        #
        #     message = consumer.consume()
        #     print(message.value.decode())
        #     # 当前消费分区offset情况
        #     print("offset_list = ",consumer.held_offsets)# {1: 5}  key为分区， 第几个




    def balance_consumer(self, offset=0):
        """
        balance consumer 消费kafka，无重复消费
        :param offset:
        :return:
        """
        # managed=True 设置后，使用新式reblance分区方法，不需要使用zk，而False是通过zk来实现reblance的需要使用zk
        consumer = self.topic.get_balanced_consumer(b"balance_consumer", managed=True, auto_commit_enable=True,auto_commit_interval_ms=1)
        partitions = self.topic.partitions
        print("partitions", partitions)
        earliest_offsets = self.topic.earliest_available_offsets()
        print("earliest_offsets", earliest_offsets)
        last_offsets = self.topic.latest_available_offsets()
        print("最近可用offset {}".format(last_offsets))
        offset = consumer.held_offsets
        print("当前消费者分区offset情况{}".format(offset))
        while True:
            msg = consumer.consume()
            offset = consumer.held_offsets
            print("{}, 当前消费者分区offset情况{}".format(msg.value.decode(), offset))
    def balance_consumer_by_id(self):
        """
        根据consumer_id消费
        :return:
        """
        consumer = self.topic.get_simple_consumer(consumer_group=b'test_group', auto_commit_enable=True,
                                             auto_commit_interval_ms=1, consumer_id=b'test_id')

        for message in consumer:
            if message is not None:
                print(message.offset, message.value.decode('utf-8'))


