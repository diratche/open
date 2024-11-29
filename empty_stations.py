from kafka import KafkaConsumer, KafkaProducer
import json
import sys

topic_in = sys.argv[1]
topic_out = sys.argv[2]

consumer = KafkaConsumer(topic_in, bootstrap_servers='localhost:9092', group_id='empty_stations', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))

empty_stations_dic = {}

for message in consumer:
    station = message.value
    name = station['name']
    available_bikes = station['totalStands']['availabilities']['bikes']
    if available_bikes == 0:
        if name not in empty_stations_dic:
            empty_stations_dic[name] = True
            producer.send(topic_out, station)
    else:
        try:
            empty_stations_dic.pop(name)
            producer.send(topic_out, station)
        except:
            pass
