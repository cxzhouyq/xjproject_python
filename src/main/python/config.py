import configparser
import os

# 加载配置文件的函数
def load_config():
    config = configparser.ConfigParser()
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在目录
    current_dir = os.path.dirname(current_file_path)
    # 拼接配置文件的绝对路径
    config_path = os.path.join(current_dir, 'resources', 'config.ini')
    config.read(config_path)
    return config
