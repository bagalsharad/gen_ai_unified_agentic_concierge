from confluent_kafka import Consumer, KafkaError
import json
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPICS = ["inventory_updates", "booking_confirmations"]

def create_consumer():
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'concierge_group',
        'auto.offset.reset': 'earliest'
    }
    return Consumer(conf)

def consume_events():
    consumer = create_consumer()
    consumer.subscribe(TOPICS)
    
    print(f"Listening to topics: {TOPICS}")
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            
            # Process event
            event_data = json.loads(msg.value().decode('utf-8'))
            print(f"Received event on {msg.topic()}: {event_data}")
            
            # TODO: Route event to Neo4j update or invalidation cache
            
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_events()
