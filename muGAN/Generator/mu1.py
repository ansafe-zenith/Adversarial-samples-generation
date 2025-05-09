"""
    Mu1-Repack
    实现 Android 应用的重新打包，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 重新打包 APK --- Apktool
        3. 对 APK 文件进行签名 --- apksigner
"""
import os
# import shutil
import subprocess
from Generator import set_path


def run_command(command):
    """ 运行系统命令并打印输出 """
    print(f"Running command: {command}")  # 执行前打印命令
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error executing {command}: {result.stderr.decode('cp936', errors='replace')}")
    else:
        print(result.stdout.decode('cp936', errors='replace'))
    print(f"Completed command: {command}")  # 执行后打印完成信息


def unpack_apk(apktool, apk_path, output_dir):
    """
        使用 Apktool 解包 APK
        示例：java -jar apktool.jar d repackage.apk -o 3
    """
    run_command(f"java -jar {apktool} d {apk_path} -f -o {output_dir}")
    print(f"APK {apk_path} unpacked to {output_dir}")


def pack_apk(apktool, input_dir, output_apk):
    """
        使用 Apktool 重打包 APK
        示例：java -jar apktool.jar b 3 -o repackage.apk
    """
    run_command(f"java -jar {apktool} b {input_dir} -o {output_apk}")
    print(f"APK {input_dir} packed to {output_apk}")


def sign_apk(zipalign, apksigner, keystore_path, keystore_pass, alias, unsigned_apk, signed_apk):
    """
        使用 apksigner 签名 APK
        示例：zipalign -v 4 repackage.apk repackageAlign.apk
             apksigner sign --ks D://Study//Generation_Algorithm//Dataset//apktool//key_apk.keystore --ks-key-alias key_apk repackageAlign.apk
    """
    run_command(f"{zipalign} -v 4 {unsigned_apk} {signed_apk}")
    run_command(f"{apksigner} sign --ks {keystore_path} --ks-pass pass:{keystore_pass} --ks-key-alias {alias} {signed_apk}")
    print(f"APK {unsigned_apk} signed to {signed_apk}")


def perturb(apk_name):
    # 配置路径
    apktool_path = set_path.apktool_path
    zipalign_path = set_path.zipalign_path
    apksigner_path = set_path.apksigner_path
    keystore = set_path.keystore
    keystore_password = set_path.keystore_password
    key_alias = set_path.key_alias

    # APK 路径
    apk_file = set_path.apk_file
    original_apk = os.path.join(apk_file, apk_name)
    output_folder = set_path.output_folder
    repacked_apk = set_path.repacked_apk
    final_signed_apk = apk_name.split('.')[0] + '_' + 'repacked.apk'

    # 解包 APK
    unpack_apk(apktool_path, original_apk, output_folder)

    # 重打包 APK
    pack_apk(apktool_path, output_folder, repacked_apk)

    # 签名 APK
    sign_apk(zipalign_path, apksigner_path, keystore, keystore_password, key_alias, repacked_apk, final_signed_apk)

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
