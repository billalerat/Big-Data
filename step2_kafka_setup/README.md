# ÉTAPE 2 Documentation

This document outlines the installation and setup process for Kafka as part of the big data project.

## Installation Steps
1. **Download Kafka** from the official website.
2. **Extract the files** to your preferred directory.
3. **Start Zookeeper** using the command:
   ```bash
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```
4. **Start Kafka** using the command:
   ```bash
   bin/kafka-server-start.sh config/server.properties
   ```

## Configuration
- Adjust the broker settings in `server.properties` to fit your requirements.
- Ensure that the `log.dirs` path is set correctly.

## Testing Kafka
- Create a topic using:
   ```bash
   bin/kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```
- Send test messages to the topic and verify the setup accordingly.