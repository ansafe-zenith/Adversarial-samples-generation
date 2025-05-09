"""
    构建 GA-GAN：
        1. 训练 Substitute Detector --- substitute.py：
            一个类似 VirusTotal 检测能力的神经网络检测器，用于评估生成的对抗样本是否能够逃脱检测
        2. 生成对抗样本 --- generators.py：
        3. 使用 Reference Detector --- reference.py：
            使用 VirusTotal 进行检测，即利用 VirusTotal API 来为生成的对抗样本做标记
        4. 构建 GAN 网络 --- ga-gan.py：
            结合生成器和检测器构建 GAN 网络
"""
import numpy as np
from tensorflow.python.keras.models import load_model

from Generator.generators import apply_perturbation
from Reference_Detectors.reference import upload_file_to_virustotal, wait_for_report, virustotal_api_key, cal_malicious
from Substitute_Detector import set_path

# 加载与训练的检测器模型
detector_model = load_model(set_path)

# GAN 参数
epochs = 10000
batch_size = 32
z_dim = 100  

for epoch in range(epochs):
    # 随机生成噪声向量
    noise = np.random.normal(0, 1, (batch_size, z_dim))

    # 生成对抗样本
    generated_apks = [apply_perturbation(f'apk_{i}.apk') for i in range(batch_size)]

    # 对抗样本检测
    detected_results = []
    for apk in generated_apks:
        upload_response = upload_file_to_virustotal(virustotal_api_key, apk)
        if upload_response:
            file_id = upload_response['data']['id']
            stats_report = wait_for_report(virustotal_api_key, file_id)
            if stats_report:
                malicious_score = cal_malicious(stats_report)
                detected_results.append(malicious_score)

    # 使用检测器进行训练
    y_fake = np.zeros((batch_size, 1))

    # 训练检测器（判别器）
    detector_model.train_on_batch(np.array(generated_apks), y_fake)

    # 打印训练进度
    if epoch % 100 == 0:
        print(f'Epoch: {epoch}, Loss: {detector_model.evaluate(np.array(generated_apks), y_fake)}')
