"""
    Mu4-Rename Method Identifier
    实现 Android 应用的重命名方法标识符，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 遍历 Smali 文件，识别并解析其中的方法标识符
        3. 为标识符生成新的随机名称
        4. 替换 Smali 文件中的所有旧标识符为新的名称
        5. 重新打包 APK --- Apktool
        6. 对 APK 文件进行签名 --- apksigner
    本段代码假设随机修改一个修饰符为 private 的 method 标识符
"""
import os
import re
import random

from Generator import set_path, mu1
from Generator.mu3 import random_identifier


def collect_private_methods(smali_folder):
    """ 收集所有 private 方法 """
    private_methods = []
    field_pattern = re.compile(r'\.method private (\w+)\(')
    for root, dirs, files in os.walk(smali_folder):
        for file_name in files:
            if file_name.endswith('.smali'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    content = file.readlines()
                for line in content:
                    match = field_pattern.search(line)
                    if match:
                        private_methods.append((file_path, match.group(1)))
    return private_methods


def rename_private_method_identifier(private_methods, existing_identifiers):
    """ 随机选择并重命名一个 private 方法 """
    if not private_methods:
        return
    file_path, original_name = random.choice(private_methods)
    new_name = random_identifier('M_', existing_identifiers)
    print("file_path: " + file_path)
    print("original_name: " + original_name)
    print("new_name: " + new_name)

    with open(file_path, 'r') as file:
        content = file.readlines()

    with open(file_path, 'w') as file:
        for line in content:
            if original_name in line:
                line = line.replace(original_name, new_name)
            file.write(line)


def perturb(apk_name):
    # 配置路径
    apktool_path = set_path.apktool_path
    zipalign_path = set_path.zipalign_path
    apksigner_path = set_path.apksigner_path
    keystore = set_path.keystore
    keystore_password = set_path.keystore_password
    key_alias = set_path.key_alias

    # APK 路径
    output_folder = set_path.output_folder
    repacked_apk = set_path.repacked_apk
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reMethod.apk'

    # 收集所有 private 方法
    print("Collecting private methods...")
    private_methods = collect_private_methods(os.path.join(output_folder, 'smali'))
    existing_identifiers = set()

    # 重命名方法标识符
    print("Renaming method identifiers...")
    rename_private_method_identifier(private_methods, existing_identifiers)

    # 重打包 APK
    mu1.pack_apk(apktool_path, output_folder, repacked_apk)

    # 签名 APK
    mu1.sign_apk(zipalign_path, apksigner_path, keystore, keystore_password, key_alias, repacked_apk, final_signed_apk)

    # 删除中间文件和目录
    if os.path.exists(repacked_apk):
        os.remove(repacked_apk)
    idsig_file = final_signed_apk + '.idsig'
    if os.path.exists(idsig_file):
        os.remove(idsig_file)

    return final_signed_apk


def main():
    apk_name = '06fd5e281179fdfad8c84a4a12977a6942b989923826f91b0bb2fc0d4c9e9641.apk'
    final_apk = perturb(apk_name)
    print("final_apk: " + final_apk)


if __name__ == '__main__':
    main()
