"""
    Mu16-Add Permission & API
    实现 Android 应用的添加权限和 API，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 添加所需权限 --- AndroidManifest.xml
        3. 添加一个使用了新增权限的方法 --- Smali
        4. 重新打包 APK --- Apktool
        5. 对 APK 文件进行签名 --- apksigner
    本段代码假设随机添加一个 Normal 级别的权限和使用了该权限的 API
"""
import os

from Generator import set_path, mu1
from Generator.mu14 import add_permission
from Generator.mu15 import add_api
from Generator.mu7 import collect_smali_files


def add_permission_api(output_file):
    """
        向 AndroidManifest.xml 随机添加一个 Normal 级别的权限
        并在 Smali 代码中添加使用该权限但永远不会执行的方法
    """
    # 添加权限
    selected_permission = add_permission(os.path.join(output_file, 'AndroidManifest.xml'))

    # 添加 API
    print("Collecting smali files...")
    smali_files = collect_smali_files(os.path.join(output_file, 'smali'))
    inject_code = [
        "    if-eqz v0, :cond_never_true\n",
        f"   const-string v0, \"{selected_permission} Used\"\n",
        "    invoke-static {v0}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I\n",
        "    :cond_never_true\n"
    ]
    print("Adding API...")
    add_api(smali_files, inject_code)


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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reAddPermAPI.apk'

    # 添加权限和 API
    print("Adding Permission and API...")
    add_permission_api(output_folder)

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
