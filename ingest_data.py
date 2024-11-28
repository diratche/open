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
producer = KafkaProducer(bootstrap_servers="localhost:9092")
while True:
  data = requests.get(address)
  if data.status_code == 200:
    producer.send(topic, data.json())
    #print(f'Ingestion successful at {time.strftime("%H:%M:%S", time.localtime())}')
  time.sleep(periodicity)
