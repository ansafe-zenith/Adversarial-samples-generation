"""
    Mu5-Rename Class Identifier
    实现 Android 应用的重命名类标识符，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 遍历 Smali 文件，识别并解析其中的类标识符
        3. 为标识符生成新的随机名称
        4. 替换 Smali 文件中的所有旧标识符为新的名称
        5. 重新打包 APK --- Apktool
        6. 对 APK 文件进行签名 --- apksigner
    本段代码假设随机修改一个 class 标识符
"""
import os
import random

from Generator import set_path, mu1
from Generator.mu3 import random_identifier


def collect_classes(smali_folder):
    """ 收集所有类的标识符 """
    class_names = []
    for root, dirs, files in os.walk(smali_folder):
        for file_name in files:
            if file_name.endswith(".smali"):
                class_names.append(os.path.join(root, file_name))
    return class_names


def rename_class_identifier(classes, existing_identifiers):
    """ 随机选择并重命名一个类 """
    if not classes:
        return
    # 随机选择一个 smali 文件
    selected_smali = random.choice(classes)
    new_name = random_identifier('C_', existing_identifiers)
    print("selected_smali: " + selected_smali)
    print("new_name: " + new_name)

    # 读取文件内容并替换类名
    with open(selected_smali, 'r') as file:
        lines = file.readlines()

    old_name, new_class_name = None, None
    for i in range(len(lines)):
        if lines[i].startswith('.class'):
            parts = lines[i].split()
            old_name = parts[-1]
            # 分割和处理原始类名
            path_parts = old_name[1:].split('/')
            base_path = '/'.join(path_parts[:-1])
            last_part = path_parts[-1]
            # 构建新类名
            new_class_name = 'L' + base_path + '/' + new_name + last_part
            lines[i] = lines[i].replace(old_name, new_class_name)
            print(f"Modified {old_name} to {new_class_name} in {selected_smali}")
            break

    if old_name and new_class_name:
        # 写回修改后的 smali 文件
        with open(selected_smali, 'w') as file:
            file.writelines(lines)

        # 更新所有其他文件的引用
        for class_name in classes:
            with open(class_name, 'r') as file:
                content = file.read()

            # 替换所有旧类名为新类名
            updated_content = content.replace(old_name, new_class_name)
            with open(class_name, 'w') as file:
                file.write(updated_content)


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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reClass.apk'

    # 收集所有类的标识符
    print("Collecting class identifiers...")
    classes = collect_classes(os.path.join(output_folder, 'smali'))
    existing_identifiers = set()

    # 重命名类标识符
    print("Renaming a random class...")
    rename_class_identifier(classes, existing_identifiers)

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
