from kafka import KafkaProducer
import requests
import json
import time
import sys

server = sys.argv[1]
key = sys.argv[2]
topic = sys.argv[3]
try:
  periodicity = sys.argv[4]
except:
  periodicity = 10

address = server + '?apiKey=' + key
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))
while True:
  response = requests.get(address)
  if response.status_code == 200:
    data = response.json()
    producer.send(topic, value=data)
    print(data)
    #print(json.dumps(data).encode('utf-8'))
    #print(f'Ingestion successful at {time.strftime("%H:%M:%S", time.localtime())}')
  time.sleep(periodicity)
