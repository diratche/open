from kafka import KafkaConsumer, TopicPartition
import json

consumer = KafkaConsumer(group_id='monitor_kafka', bootstrap_servers='localhost:9092')

while True:
  topic_list = consumer.topics()
  for topic in topic_list:
      partition_id_list = consumer.partitions_for_topic(topic)
      for partition_id in partition_id_list:
          consumer.assign([TopicPartition(topic, partition_id)])
          consumer.seek_to_end()
          for message in consumer:
              timestamp = message.timestamp
              break
          offset_id = list(consumer.end_offsets([TopicPartition(topic, partition_id)]).values())[0]
          print(f'Topic-name={topic}, Partition-id={partition_id}, offset-id={offset_id}, timestamp={timestamp}')

