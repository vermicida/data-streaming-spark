from config import KafkaConfig
from kafka import KafkaConsumer
from logger import get_logger

logger = get_logger(__name__)


def run_consumer():

    ''' Read the messages from a Kafka topic '''

    options = {
        'bootstrap_servers': KafkaConfig.external_servers,
        'auto_offset_reset': 'earliest',
        'consumer_timeout_ms': 1000
    }

    consumer = KafkaConsumer(**options)

    consumer.subscribe([KafkaConfig.topic])

    for message in consumer:
        logger.info(message.value)


if __name__ == '__main__':
    run_consumer()
