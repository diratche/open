from kafka import KafkaConsumer, KafkaProducer
import json
import sys

topic_in = sys.argv[1]

consumer = KafkaConsumer(topic_in, bootstrap_servers='localhost:9092', group_id='alert_empty_stations', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))

empty_stations_dic = {}

for message in consumer:
    available_bikes = station['totalStands']['availabilities']['bikes']
    city = station['contractName']
    address = station['address']
    if available_bikes == 0:
        print(city, address)
