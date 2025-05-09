"""
    Mu15-Add API
    实现 Android 应用的添加 API，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 定义一个永远不满足的分支
        3. 选择一个方法进行修改 --- Smali
        4. 重新打包 APK --- Apktool
        5. 对 APK 文件进行签名 --- apksigner
"""
import os
import random

from Generator import set_path, mu1
from Generator.mu7 import collect_smali_files


def add_api(smali_files, inject_code):
    """ 在 Smali 文件中随机添加一个永远不会执行的 API """
    if not smali_files:
        return
    selected_smali = random.choice(smali_files)
    print("selected_smali: " + selected_smali)

    with open(selected_smali, 'r') as file:
        lines = file.readlines()

    # 在文件中找到 .method 标记的开始和结束
    method_indices = [i for i, line in enumerate(lines) if line.strip().startswith('.method')]
    if not method_indices:
        return
    print("method_indices:")
    print(method_indices)

    selected_smali_index = random.choice(method_indices)
    # 在选择的方法中添加永远不会执行的代码
    inject_index = selected_smali_index + 1
    while inject_index < len(lines) and lines[inject_index].strip() != '.prologue':
        inject_index += 1

    # 如果没有找到 .prologue，选择合适的位置插入代码
    if inject_index >= len(lines) or lines[inject_index].strip() != '.prologue':
        # 如果整个方法中都没有 .prologue，我们可以选择在 .locals 或第一个指令前插入
        inject_index = selected_smali_index + 1
        while inject_index < len(lines) and not lines[inject_index].strip().startswith('.locals') and not lines[inject_index].strip().startswith('invoke-'):
            inject_index += 1

    # 插入一个永远不会执行的条件分支
    lines[inject_index:inject_index] = inject_code

    with open(selected_smali, 'w') as file:
        file.writelines(lines)


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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reAddAPI.apk'

    # 收集所有类的标识符
    print("Collecting smali files...")
    smali_files = collect_smali_files(os.path.join(output_folder, 'smali'))

    # 定义条件分支
    inject_code = [
        "    if-eqz v0, :cond_never_true\n",
        "    const-string v0, \"Never Executed\"\n",
        "    invoke-static {v0}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I\n",
        "   :cond_never_true\n"
    ]

    # 添加 API
    print("Adding API...")
    add_api(smali_files, inject_code)

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
