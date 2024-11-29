from kafka import KafkaConsumer
import json
import sys

topic_in = sys.argv[1]

consumer = KafkaConsumer(topic_in, bootstrap_servers='localhost:9092', group_id='archive_data', value_deserializer=lambda x: json.loads(x.decode('utf-8')))

with open('archive.txt', 'w') as archive:
    for message in consumer:
        station = message.value
        print(station, file=archive)
