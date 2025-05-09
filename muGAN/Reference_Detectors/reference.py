"""
    使用黑盒检测器对生成的对抗样本添加标记：
        黑盒检测器 --- VirusTool
        标记 --- 恶意 (1) 或良性 (0)
    注 1 --- VirusTotal 相关信息如下所示：
        API KEY: 169d3b77091cf49775f723ca99feabdbbb336650ae2d912889f3dd0cf3119588
    注 2 --- 运行前先关闭“控制面板”中的“代理服务器”

    运行出错：
        requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None))
        VirusTool 不允许将 API KEY 写入脚本
"""
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def create_session(retries=3, backoff_factor=0.3):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 503, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def upload_file_to_virustotal(api_key, apk_path):
    url = 'https://www.virustotal.com/api/v3/files'
    headers = {'x-apikey': api_key}
    session = create_session()

    with open(apk_path, 'rb') as file:
        files = {'file': (apk_path, file)}
        response = session.post(url, headers=headers, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Upload failed with status code {response.status_code}: {response.text}")
            return None


def get_report(api_key, apk_id):
    url = f'https://www.virustotal.com/api/v3/analyses/{apk_id}'
    headers = {'x-apikey': api_key}
    session = create_session()
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Get report failed with status code {response.status_code}: {response.text}")
        return None


def wait_for_report(api_key, apk_id, max_attempts=20, sleep_interval=60):
    attempts = 0
    while attempts < max_attempts:
        report = get_report(api_key, apk_id)
        if report and 'data' in report and 'attributes' in report['data'] and 'status' in report['data']['attributes']:
            status = report['data']['attributes']['status']
            if status == 'completed':
                # 提取并返回 stats 数据
                if 'stats' in report['data']['attributes']:
                    stats = report['data']['attributes']['stats']
                    return stats
        # 等待指定的事件后再次尝试
        time.sleep(sleep_interval)
        attempts += 1
    return None


def cal_malicious(stats):
    """ 计算恶意性 """
    mal = stats.get('malicious', 0)
    total = sum(value for key, value in stats.items())
    return mal / total if total != 0 else 0


virustotal_api_key = '169d3b77091cf49775f723ca99feabdbbb336650ae2d912889f3dd0cf3119588'
apk_file = 'D://apktool//Drebin//02-Adrd//addApi.apk'
# 判断是良性还是恶意的标签
label = ''

# 上传文件并获取响应
upload_response = upload_file_to_virustotal(virustotal_api_key, apk_file)

if upload_response:
    print("File upload successfully.")
    file_id = upload_response['data']['id']

    # 等待报告并打印
    stats_report = wait_for_report(virustotal_api_key, file_id)
    if stats_report:
        malicious = cal_malicious(stats_report)
        # print("malicious: " + str(malicious))
        if malicious > 0.5:
            label = 'malicious'
        else:
            label = 'benign'
        print("label: " + label)
        # print("Statistics from the security report:")
        # for key, value in stats_report.items():
        #     print(f"{key}: {value}")
    else:
        print("Failed to get the security report after several attempts.")
else:
    print("File upload failed.")
