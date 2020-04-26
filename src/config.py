import configparser
import os

_here = os.path.split(os.path.abspath(__file__))[0]

# Load the configuration.
_config = configparser.ConfigParser()
_config.read(os.path.join(_here, 'config', 'config.ini'))


def _get_data_path(filename):

    ''' Get the absolute path of the given data file '''

    return os.path.join(_here, 'data', filename)


class KafkaConfig:
    external_servers = _config.get('kafka', 'external-servers')
    internal_servers = _config.get('kafka', 'internal-servers')
    topic = _config.get('kafka', 'topic')
    client_id = _config.get('kafka', 'client-id')


class SparkConfig:
    master = _config.get('spark', 'master')
    app_name = _config.get('spark', 'app-name')


class DataConfig:
    sfdpd_calls = _get_data_path(_config.get('data', 'sfpd-calls'))
    sfdpd_codes = _get_data_path(_config.get('data', 'sfpd-codes'))
