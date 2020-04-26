import json
import time
from kafka import KafkaProducer
from logger import get_logger

logger = get_logger(__name__)


class ProducerServer(KafkaProducer):

    def __init__(self, input_file, topic, sleep=2, **kwargs):

        ''' Class constructor '''

        super().__init__(**kwargs)
        self.input_file = input_file
        self.topic = topic
        self.sleep = sleep

    def generate_data(self):

        ''' Send the messages read from the input file to the Kafka topic '''

        for message in self.read_messages(self.input_file):
            logger.info(message)
            self.send(self.topic, message)
            time.sleep(self.sleep)

    @classmethod
    def read_messages(cls, path):

        ''' Read the messages from the given JSON file '''

        for item in cls.load_json_file(path):
            yield cls.dict_to_binary(item)

    @classmethod
    def load_json_file(cls, path):

        ''' Load a JSON file from the given path '''

        with open(path, 'r') as f:
            data = json.load(f)
        return data

    @classmethod
    def dict_to_binary(cls, data):

        ''' Encode the given dictionary as a binary string '''

        return json.dumps(data).encode('utf-8')
