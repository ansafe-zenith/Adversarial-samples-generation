"""
    Mu2-Rename Package
    实现 Android 应用的重命名包名，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 修改目录结构 -- 在 Smali 文件目录中重构目录结构
        3. 重命名 Smali 文件中的包名 --- 在所有 Smali 文件中搜索旧包名并替换为新包名
        4. 重命名 AndroidManifest.xml 文件中的包名 --- 更新应用的包名
        5. 重新打包 APK --- Apktool
        6. 对 APK 文件进行签名 --- apksigner
"""
import os
import re
import shutil
import xml.etree.ElementTree as ET

from Generator import set_path, mu1


def extract_package_name(manifest):
    """ 从 AndroidManifest.xml 中提取包名 """
    tree = ET.parse(manifest)
    root = tree.getroot()
    package_name = root.attrib['package']
    return package_name


def set_package_name(old_name):
    """ 设置新包名 """
    split_name = old_name.split(".")
    count = len(split_name)
    new_name = ''
    if count == 2:
        new_name = 're.name'
    elif count == 3:
        new_name = 're.name.package'
    elif count == 4:
        new_name = 're.name.package.mu'
    return new_name


def update_smali_files(smali, old_package, new_package):
    """ 更新 Smali 文件中的包名 """
    old_path = old_package.replace('.', '/')
    new_path = new_package.replace('.', '/')

    # 更新 Smali 文件内容
    for root, dirs, files in os.walk(smali):
        for file_name in files:
            if file_name.endswith('.smali'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()
                content = content.replace(old_path, new_path)
                with open(file_path, 'w') as file:
                    file.write(content)

    # 重命名目录
    original_path = os.path.join(smali, old_path)
    target_path = os.path.join(smali, new_path)
    if os.path.exists(original_path):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.move(original_path, target_path)


def update_android_manifest(manifest, new_package):
    """ 更新 AndroidManifest.xml 中的包名 """
    with open(manifest, 'r') as file:
        content = file.read()
    content = re.sub(r'package="[^"]+"', f'package="{new_package}"', content)
    with open(manifest, 'w') as file:
        file.write(content)


def rename_package(smali, manifest, old_package, new_package):
    """ 更新包名 """
    update_smali_files(smali, old_package, new_package)
    update_android_manifest(manifest, new_package)


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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'repackage.apk'

    # 需要修改部分的路径
    manifest_path = os.path.join(output_folder, 'AndroidManifest.xml')
    smali_folder = os.path.join(output_folder, 'smali')
    old_package_name = extract_package_name(manifest_path)
    new_package_name = set_package_name(old_package_name)

    # 重命名包名
    rename_package(smali_folder, manifest_path, old_package_name, new_package_name)

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
