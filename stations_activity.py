from kafka import KafkaConsumer, KafkaProducer


consumer = KafkaConsumer(topic_in, bootstrap_servers='localhost:9092', group_id='app1', value_serializer=str.decode)
producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=str.encode)


