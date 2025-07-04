"""
此模块使用 WxPusher 实现错误消息通知功能
"""
import requests
from notify_config import WXPUSHER_APP_TOKEN, WXPUSHER_TOPIC_IDS, WXPUSHER_UIDS


def send_error_notification(error_message: str):
    """
    发送错误消息通知到 WxPusher

    :param error_message: 要发送的错误消息内容
    """
    # 检查是否配置了 topic_ids 或 uids
    if not WXPUSHER_TOPIC_IDS and not WXPUSHER_UIDS:
        raise ValueError("topic_ids 与 uids 至少配置一个才行")

    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": WXPUSHER_APP_TOKEN,
        "content": error_message,
        "contentType": 1,
    }

    if WXPUSHER_TOPIC_IDS:
        data["topicIds"] = [int(x) for x in WXPUSHER_TOPIC_IDS.split(';') if x.strip()]
    if WXPUSHER_UIDS:
        data["uids"] = [x.strip() for x in WXPUSHER_UIDS.split(';') if x.strip()]
    # 打印uid 和topicIds
    print(f"uids: {data['uids']}")
    try:
        response = requests.post(url, json=data)
        print(f"response: {response.text}")
        response.raise_for_status()
        result = response.json()
        if result.get("code") != 1000:
            raise Exception(f"消息发送失败: {result.get('msg')}")
        return result
    except requests.RequestException as e:
        raise Exception(f"网络请求出错: {str(e)}")