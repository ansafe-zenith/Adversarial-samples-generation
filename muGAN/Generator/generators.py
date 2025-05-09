"""
    生成器的实现 --- 从 16 种预定义的方法中选择一个生成对抗性恶意软件样本：
        输入 --- 恶意软件样本 + 扰动方法
        方法 --- 从 16 种预定义的方法中选择一个应用
        输出 --- 对抗样本
"""
import os.path
import random
import shutil
import subprocess

from Generator import mu1, mu2, mu3, mu4, mu5, mu6, mu7, mu8, mu9, mu10, mu11, mu12, mu13, mu14, mu15, mu16, set_path


def apply_perturbation(apk_name):
    """ 随机选择并应用一个扰动方法 """
    apktool_path = set_path.apktool_path
    apk_file = set_path.apk_file
    original_apk = os.path.join(apk_file, apk_name)
    output_folder = set_path.output_folder
    mu1.unpack_apk(apktool_path, original_apk, output_folder)

    final_apk = ''
    method_index = random.randint(1, 16)
    apk_count = 5
    num = 0
    while num < apk_count:
        if method_index == 1:
            final_apk = mu1.perturb(apk_name)
        elif method_index == 2:
            final_apk = mu2.perturb(apk_name)
        elif method_index == 3:
            final_apk = mu3.perturb(apk_name)
        elif method_index == 4:
            final_apk = mu4.perturb(apk_name)
        elif method_index == 5:
            final_apk = mu5.perturb(apk_name)
        elif method_index == 6:
            final_apk = mu6.perturb(apk_name)
        elif method_index == 7:
            final_apk = mu7.perturb(apk_name)
        elif method_index == 8:
            final_apk = mu8.perturb(apk_name)
        elif method_index == 9:
            final_apk = mu9.perturb(apk_name)
        elif method_index == 10:
            final_apk = mu10.perturb(apk_name)
        elif method_index == 11:
            final_apk = mu11.perturb(apk_name)
        elif method_index == 12:
            final_apk = mu12.perturb(apk_name)
        elif method_index == 13:
            final_apk = mu13.perturb(apk_name)
        elif method_index == 14:
            final_apk = mu14.perturb(apk_name)
        elif method_index == 15:
            final_apk = mu15.perturb(apk_name)
        elif method_index == 16:
            final_apk = mu16.perturb(apk_name)

        # 保存当前生成的 APK 文件
        apk_folder = os.path.join(set_path.apk_file, 'Generator//' + final_apk)
        samples_file = set_path.samples_file
        # save_apk(apk_folder, samples_file)
        save_apk_if_installed(os.path.join(apk_file, apk_name), samples_file)

        if method_index != 16:
            method_index += 1
        else:
            method_index = 1
        num += 1

    # 删除残留的目录
    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)

    return final_apk


def install_apk_to_nox(apk_path):
    """ 生成的 APK 文件是否可以安装到模拟器 """
    # return True
    # 尝试连接到夜神模拟器
    subprocess.run(['adb', 'connect', '127.0.0.1:62001'])

    # 安装 APK 到夜神模拟器
    try:
        result = subprocess.run(['adb', '-s', '127.0.0.1:62001', 'install', apk_path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        if 'Success' in output:
            return True
        else:
            return False
    except Exception as e:
        print(f"安装过程中出错：{e}")
        return False


def save_apk_if_installed(apk_path, samples_folder):
    """ 如果 APK 成功安装，则保存到 Samples 文件夹 """
    if install_apk_to_nox(apk_path):
        # 确保 Samples 文件夹存在
        if not os.path.exists(samples_folder):
            os.makedirs(samples_folder)
        # 计算目标路径
        target_path = os.path.join(samples_folder, os.path.basename(apk_path))
        # 复制文件
        shutil.copy(apk_path, target_path)
        print(f"APK 安装成功，已保存到 {target_path}")
    else:
        print(f"APK [{apk_path}] 安装失败，不进行保存")


def save_apk(apk_path, samples_folder):
    """ 保存所有生成的 APK 文件到 Samples 文件夹 """
    # 确保 Samples 文件夹存在
    if not os.path.exists(samples_folder):
        os.makedirs(samples_folder)
    # 计算目标路径
    target_path = os.path.join(samples_folder, os.path.basename(apk_path))
    # 复制文件
    shutil.copy(apk_path, target_path)
    print(f"APK 安装成功，已保存到 {target_path}")


def adversarial_samples(folder_path):
    """ 整个文件夹生成对抗样本 """
    for apk_name in os.listdir(folder_path):
        if apk_name.endswith('.apk'):
            apply_perturbation(apk_name)


def main():
    """ TEST: 一个 APK 文件的情况 """
    # apk_name = '06fd5e281179fdfad8c84a4a12977a6942b989923826f91b0bb2fc0d4c9e9641.apk'
    # apply_perturbation(apk_name)

    # 整个文件夹的情况
    dataset_path = set_path.dataset_folder
    adversarial_samples(dataset_path)


if __name__ == '__main__':
    main()
