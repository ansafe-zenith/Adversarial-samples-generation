"""
    数据收集与预处理：
        1. 获取 APK 标签 --- 良性应用和恶意应用分别存储在 benign 和 malicious 两个文件夹中
        2. 提取 APK 文件的静态特征并添加标签 --- permissions、API calls、Intent-filters
        3. 将提取到的信息保存到 CSV 文件中
"""
import os
import pandas as pd
import logging
from androguard.misc import AnalyzeAPK

from Substitute_Detector import set_path

# 设置日志记录
logging.basicConfig(filename=set_path.errors_log_path, level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s')

# 定义 APK 文件夹路径
benign_apk_dir = set_path.benign_apk_path
malicious_apk_dir = set_path.malicious_apk_path

# 获取 APK 文件路径
benign_apk_files = [os.path.join(benign_apk_dir, f) for f in os.listdir(benign_apk_dir) if f.endswith('.apk')]
malicious_apk_files = [os.path.join(malicious_apk_dir, f) for f in os.listdir(malicious_apk_dir) if f.endswith('.apk')]

# 遍历 APK 文件夹
# apk_dir = '/path/to/apk/files'
# apk_files = [os.path.join(apk_dir, f) for f in os.listdir(apk_dir) if f.endswith('.apk')]


def extract_features(apk_path):
    """ 提取特征函数 """
    try:
        a, d, dx = AnalyzeAPK(apk_path)
        permissions = a.get_permissions()

        api_calls = set()
        for method in dx.get_methods():
            for _, call, _ in method.get_xref_to():
                api_calls.add(call.class_name + '->' + call.name)

        intents = []
        for component in a.get_activities() + a.get_services() + a.get_receivers():
            intent_filters = a.get_intent_filters(component, 'activity')  # 调整itemtype
            for intent_filter in intent_filters:
                intents.extend(intent_filter.get('actions', []))

        # 将特征转换为字符串，以便存储在CSV文件中
        return {
            'apk_path': apk_path,
            'permissions': ' '.join(permissions),
            'api_calls': ' '.join(api_calls),
            'intent_filters': ' '.join(intents),
        }
    except Exception as e:
        logging.error(f"Error processing {apk_path}: {e}")
        # print(f"Error processing {apk_path}: {e}")
        return None
    # activities = a.get_activities()
    # services = a.get_services()
    # receivers = a.get_receivers()
    # 更多特征提取代码
    # return {
    #     'apk_path': apk_path,
    #     'permissions': permissions,
    #     'activities': activities,
    #     'services': services,
    #     'receivers': receivers,
    # }


def extract_features_with_label(apk_files, label):
    """ 提取并添加标签的辅助函数 """
    features = []
    for apk in apk_files:
        feature = extract_features(apk)
        if feature:
            feature['label'] = label
            features.append(feature)
    return features


# 提取良性应用的特征并添加标签
benign_features = extract_features_with_label(benign_apk_files, 'benign')

# 提取恶意软件的特征并添加标签
malicious_features = extract_features_with_label(malicious_apk_files, 'malware')

# 提取良性应用的特征并添加标签
# benign_features = [extract_features(apk) for apk in benign_apk_files]
# for feature in benign_features:
#     feature['label'] = 'benign'

# 提取恶意软件的特征并添加标签
# malicious_features = [extract_features(apk) for apk in malicious_apk_files]
# for feature in malicious_features:
#     feature['label'] = 'malware'

# 合并所有特征
all_features = benign_features + malicious_features

# 转换为 DataFrame
df = pd.DataFrame(all_features)

# 保存为 CSV 文件
df.to_csv(set_path.features_csv_path, index=False)

print("Feature extraction complete. Errors are logged in 'apk_processing_errors.log'.")
