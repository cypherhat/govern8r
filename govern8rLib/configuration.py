import configparser
import os

file_name = 'notaryconfig.ini'


def config_exists():
    if os.path.exists(file_name) and os.path.isfile(file_name):
        return True
    else:
        return False


def read_configuration():
    if config_exists():
        config = configparser.ConfigParser()
        config.read(file_name)
        return config


class NotaryConfiguration(object):
    """An encapsulated configuration reading.
    """

    def __init__(self, sect):
        if not config_exists():
            raise ValueError('Configuration does not exist!')
        self.sectionName = sect
        self.config = read_configuration()

    def get_block_cypher_url(self):
        if self.config.has_option(self.sectionName, 'block_cypher_url'):
            return self.config.get(self.sectionName, 'block_cypher_url')
        else:
            raise ValueError('Value does not exist!')

    def get_server_url(self):
        if self.config.has_option(self.sectionName, 'server_url'):
            return self.config.get(self.sectionName, 'server_url')
        else:
            raise ValueError('Value does not exist!')

    def get_db_url(self):
        if self.config.has_option(self.sectionName, 'db_url'):
            return self.config.get(self.sectionName, 'db_url')
        else:
            raise ValueError('Value does not exist!')

    def get_wallet_name(self):
        if self.config.has_option(self.sectionName, 'wallet_name'):
            return self.config.get(self.sectionName, 'wallet_name')
        else:
            raise ValueError('Value does not exist!')

    def get_wallet_password(self):
        if self.config.has_option(self.sectionName, 'wallet_password'):
            return self.config.get(self.sectionName, 'wallet_password')
        else:
            raise ValueError('Value does not exist!')

    def get_block_cypher_token(self):
        if self.config.has_option(self.sectionName, 'block_cypher_token'):
            return self.config.get(self.sectionName, 'block_cypher_token')
        else:
            raise ValueError('Value does not exist!')
