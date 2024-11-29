from kafka import KafkaConsumer, KafkaProducer
import json
import sys

topic_in = sys.argv[1]
topic_out = sys.argv[2]

consumer = KafkaConsumer(topic_in, bootstrap_servers='localhost:9092', group_id='stations_activity', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))

station_status_list = {}

for message in consumer:
    station = message.value
    try:
        available_bikes = station_status_list[station['name']]['bikes']
        available_stands = station_status_list[station['name']]['stands']
        if station['totalStands']['availabilities']['bikes'] != available_bikes or station['totalStands']['availabilities']['stands'] != available_stands:
            station_status_list[station['name']] = {'bikes': station['totalStands']['availabilities']['bikes'], 'stands': station['totalStands']['availabilities']['stands']}
            producer.send(topic_out, station)
    except KeyError:
        available_bikes = station['totalStands']['availabilities']['bikes']
        available_stands = station['totalStands']['availabilities']['stands']
        station_status_list[station['name']] = {'bikes': available_bikes, 'stands': available_stands}
        producer.send(topic_out, station)
