#!/bin/bash
# Shell script to create Kafka topics

# Replace with your Kafka broker address
BROKER_ADDRESS="localhost:9092"

# Create first topic
kafka-topics.sh --create --topic my_first_topic --bootstrap-server $BROKER_ADDRESS --partitions 1 --replication-factor 1

# Create second topic
kafka-topics.sh --create --topic my_second_topic --bootstrap-server $BROKER_ADDRESS --partitions 1 --replication-factor 1

echo "Topics created successfully!"