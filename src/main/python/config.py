import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    return config
