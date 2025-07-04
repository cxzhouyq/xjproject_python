import time
import requests
import random
from datetime import datetime
from config import load_config
from utils import log_info, log_error
from notify import send_error_notification
from apscheduler.schedulers.blocking import BlockingScheduler



def post_xj():
    fails = []
    weekday = datetime.today().weekday()  # Monday=0 ... Sunday=6
    
    # 从配置获取数据
    config = load_config()
    xj_users = config['XJ']['users'].split(',')
    xj_domains = config['XJ']['domains'].split(',')
    ym_domains = config['YM']['domains'].split(',')
    
    # 定义URL模板
    urls = [
        config['URL_TEMPLATES']['box'],
        config['URL_TEMPLATES']['box6'],
        config['URL_TEMPLATES']['sign'],
        config['URL_TEMPLATES']['qrcode'],
        config['URL_TEMPLATES']['click'],
        config['URL_TEMPLATES']['pl']
    ]
    for url_template in urls:
        for user_entry in xj_users:
            user_type, cookie = user_entry.split('_', 1)
            
            # 检查周六条件
            if "taskid=1622" in url_template and weekday != 5:  # 5=Saturday
                continue
                
            # 选择域名池
            domains = xj_domains if user_type == 'xj' else ym_domains
            
            for domain in domains:
                url = ''
                try:
                    # 特殊处理 pl 模板
                    if 'comment' in url_template:
                        url = url_template.format(domain, random.randint(1, 1000))
                    else:
                        url = url_template.format(domain)
                        
                    headers = {
                        'X-Cookie-Auth': cookie,
                        'user-agent': 'Dio/4.1.8 Android'
                    }
                    
                    log_info(f"请求url: {url}")
                    time.sleep(1)  # 间隔1秒
                    log_info(f"用户信息[{user_entry}]")
                    response = requests.post(url, headers=headers)
                    log_info(f"Response Body: {response.text}")
                    
                    if response.status_code == 200:
                        break
                    elif domain == domains[-1]:
                        fails.append(f"{url}({user_entry})请求失败！")
                        
                except Exception as e:
                    log_error(e)
                    if domain == domains[-1]:
                        fails.append(f"{url}({user_entry})请求失败！")
    
    return fails


def post_vip():
    config = load_config()
    users = config['DEFAULT']['users'].split(',')
    domains = config['DEFAULT']['domains'].split(',')
    log_info(f"users: {users}")
    log_info(f"domains: {domains}")
    fails = []
    for domain in domains:
        for user in users:
            headers = {
                'X-Access-Token': user,
                'user-agent': 'Dio/4.1.8 Android'
            }
            try:
                response = requests.post(domain, headers=headers)
                log_info(f"请求url: {domain}")
                log_info(f"Response Body: {response.text}")
                if response.status_code != 200:
                    fails.append(f"{domain}({user})请求失败！")
            except Exception as e:
                fails.append(f"{domain}({user})请求失败！")
                log_error(e)
    return fails

def xj_sign():
    fails = post_xj()
    if fails:
        log_error("\n".join(fails))
        send_error_notification("\n".join(fails))
    else:
        log_info("执行完成")
        send_error_notification("执行完成")

def vip_sign():
    fails = post_vip()
    if fails:
        log_error("\n".join(fails))
        send_error_notification("\n".join(fails))
    else:
        log_info("执行完成")
        send_error_notification("执行完成")

if __name__ == "__main__":

     
    # 立即执行一次
    xj_sign()
    vip_sign()

    scheduler = BlockingScheduler()
    scheduler.add_job(xj_sign, 'interval', minutes=30)  # 每30分钟执行一次 xj_sign
    scheduler.add_job(vip_sign, 'interval', minutes=60)  # 每60分钟执行一次 vip_sign

    # 每天 10:01 执行
    scheduler.add_job(xj_sign, 'cron', hour=22, minute=1)
    scheduler.add_job(vip_sign, 'cron', hour=7, minute=2)
    log_info('ddddddd')
    scheduler.start()
