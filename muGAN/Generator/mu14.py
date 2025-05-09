"""
    Mu14-Add Permission
    实现 Android 应用的添加权限，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 添加所需权限 --- AndroidManifest.xml
        3. 重新打包 APK --- Apktool
        4. 对 APK 文件进行签名 --- apksigner
    本段代码假设随机添加一个 Normal 级别的权限
"""
import os
import random
import xml.etree.ElementTree as ET

from Generator import set_path, mu1


def add_permission(manifest_path):
    """ 向 AndroidManifest.xml 随机添加一个 Normal 级别的权限 """
    selected_permission = random.choice(set_path.normal_permissions)
    print("selected_permission:" + selected_permission)

    tree = ET.parse(manifest_path)
    root = tree.getroot()

    # 创建新的权限元素
    new_permission = ET.Element("uses-permission")
    new_permission.set("{http://schemas.android.com/apk/res/android}name", selected_permission)

    # 添加新权限到根元素
    root.append(new_permission)

    # 保存修改后的 XML 文件
    tree.write(manifest_path)
    return selected_permission


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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reAddPerm.apk'

    # 添加权限
    print("Adding Permission...")
    add_permission(os.path.join(output_folder, 'AndroidManifest.xml'))

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
