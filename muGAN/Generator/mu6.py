"""
    Mu6-Rename Resource
    实现 Android 应用的重命名资源文件，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 遍历 res 文件，识别并解析其中的资源文件
        3. 随机选择一个资源文件
        4. 在资源的引用处更新资源名称
        5. 重新打包 APK --- Apktool
        6. 对 APK 文件进行签名 --- apksigner
    本段代码假设随机修改一个资源文件名
"""
import os
import random

from Generator import set_path, mu1
from Generator.mu3 import random_identifier


def collect_resources(res_folder):
    """ 收集所有资源文件的路径 """
    res_files = []
    for root, dirs, files in os.walk(res_folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.xml', '.txt')):
                res_files.append(os.path.join(root, file))
    return res_files


def updated_resource(res_folder, old_name, new_name):
    """ 遍历目录，更新资源引用 """
    for root, dirs, files in os.walk(res_folder):
        for file_name in files:
            if file_name.endswith('.xml'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.read()

                # 检查文件中是否有旧的资源名
                if old_name in lines:
                    updated_line = lines.replace(old_name, new_name)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(updated_line)
                    print(f"Updated {file_path}")


def rename_resource(res_files, existing_res, res_folder):
    """ 随机选择并重命名一个资源文件 """
    if not res_files:
        return
    # 随机选择一个资源文件
    selected_res = random.choice(res_files)
    print("selected_res: " + selected_res)

    # 生成新的文件名
    file_path, ext = os.path.splitext(selected_res)
    new_name = random_identifier('_R_', existing_res)
    new_res_name = file_path + new_name + ext
    print("file_path: " + file_path)
    print("ext: " + ext)
    print("new_res_name: " + new_res_name)
    os.rename(selected_res, new_res_name)
    print(f"Renamed {selected_res} to {new_res_name}")

    # updated_resource(res_folder, selected_res, os.path.basename(new_res_name))


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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reResource.apk'

    # 收集所有类的标识符
    print("Collecting resources...")
    resources = collect_resources(os.path.join(output_folder, 'res'))
    existing_identifiers = set()

    # 重命名资源文件
    print("Renaming a random resource...")
    rename_resource(resources, existing_identifiers, os.path.join(output_folder, 'res'))

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
