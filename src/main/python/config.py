import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('src/main/resources/config.ini')
    return config
