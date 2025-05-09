"""
    Mu13-Modify API Level
    实现 Android 应用的替换低版本的 API，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 修改 AndroidManifest.xml 文件 --- android:minSdkVersion 和 android:targetSdkVersion 属性
        3. 重新打包 APK --- Apktool
        4. 对 APK 文件进行签名 --- apksigner
"""
import os
import xml.etree.ElementTree as ET

from Generator import set_path, mu1


def modify_api_level(manifest_path):
    """ 将 AndroidManifest.xml 中的 minSdkVersion 和 targetSdkVersion 统一降低 1 """
    tree = ET.parse(manifest_path)
    root = tree.getroot()

    # 查找并修改 <uses-sdk> 标签的属性
    for uses_sdk in root.findall('uses-sdk'):
        min_sdk_attr = '{http://schemas.android.com/apk/res/android}minSdkVersion'
        target_sdk_attr = '{http://schemas.android.com/apk/res/android}targetSdkVersion'
        if uses_sdk.get(min_sdk_attr):
            current_min_sdk = uses_sdk.get(min_sdk_attr)
            new_min_sdk = str(int(current_min_sdk) - 1)
            uses_sdk.set(min_sdk_attr, new_min_sdk)
            print(f"Modified min_sdk_attr API level from {current_min_sdk} to {new_min_sdk}")
        if uses_sdk.get(target_sdk_attr):
            current_target_sdk = uses_sdk.get(target_sdk_attr)
            new_target_sdk = str(int(current_target_sdk) - 1)
            uses_sdk.set(target_sdk_attr, new_target_sdk)
            print(f"Modified target_sdk_attr API level from {current_target_sdk} to {new_target_sdk}")

    # 保存修改后的 XML 文件
    tree.write(manifest_path)


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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reModifyAPI.apk'

    # 修改 Android 的版本
    print("Modifying API level...")
    modify_api_level(os.path.join(output_folder, 'AndroidManifest.xml'))

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
