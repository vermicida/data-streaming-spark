from config import DataConfig, KafkaConfig
from logger import get_logger
from producer_server import ProducerServer

logger = get_logger(__name__)


def run_producer():

    ''' Simulate emergency calls to the S.F.P.D. '''

    options = {
        'input_file': DataConfig.sfdpd_calls,
        'topic': KafkaConfig.topic,
        'bootstrap_servers': KafkaConfig.internal_servers,
        'client_id': KafkaConfig.client_id
    }

    producer = ProducerServer(**options)

    try:
        logger.info('Starting producer {}'.format(KafkaConfig.client_id))
        producer.generate_data()
    except KeyboardInterrupt:
        logger.info('Stopping producer {}'.format(KafkaConfig.client_id))
    finally:
        producer.close()


if __name__ == '__main__':
    run_producer()
