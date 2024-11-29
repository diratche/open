from kafka import KafkaConsumer
import json
import sys
import time

topic_in = sys.argv[1]

consumer = KafkaConsumer(topic_in, bootstrap_servers='localhost:9092', group_id='alert_empty_stations', value_deserializer=lambda x: json.loads(x.decode('utf-8')))

empty_stations_dic = {}

for message in consumer:
    station = message.value
    available_bikes = station['totalStands']['availabilities']['bikes']
    city = station['contractName']
    name = station['name']
    address = station['address']
    if available_bikes == 0:
        print(time.strftime("%H:%M:%S", time.localtime()), city, name, address)
