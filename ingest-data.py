from kafka import KafkaProducer
import requests
import json
import time

def ingest_data(server, key, topic, periodicity=10):
  address = server + '?apiKey=' + key
  producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=str.encode)
  while True:
    data = requests.get(address)
    if data.status_code == 200:
      producer.send(topic, json.dump(data.json()).encode('utf-8'))
      print(f'Ingestion successful at {time.strftime("%d %H:%M:%S", time.localtime())}')
    time.sleep(periodicity)
