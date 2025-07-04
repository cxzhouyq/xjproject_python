# wxpusher 配置
import configparser
import os

# 读取配置文件
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'config.ini')
config.read(config_path, encoding='utf-8')

# 从配置文件获取wxpusher相关配置
WXPUSHER_APP_TOKEN = config.get('WXPUSHER', 'app_token')  # wxpusher 的 appToken 官方文档: https://wxpusher.zjiecode.com/docs/
WXPUSHER_TOPIC_IDS = config.get('WXPUSHER', 'topic_ids')  # wxpusher 的 主题ID，多个用英文分号;分隔 topic_ids 与 uids 至少配置一个才行
WXPUSHER_UIDS = config.get('WXPUSHER', 'uids')            # wxpusher 的 用户ID，多个用英文分号;分隔 topic_ids 与 uids 至少配置一个才行