"""
    Mu8-Encode Data
    实现 Android 应用的数据加密，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 随机选择 Smali 文件中的一个字符串常量
        3. 加密该字符串常量 --- Base64 编码
        4. 重新打包 APK --- Apktool
        5. 对 APK 文件进行签名 --- apksigner
"""
import base64
import os
import random

from Generator import set_path, mu1
from Generator.mu7 import collect_smali_files


def encode_string(smali_files):
    """ 随机选择并进行数据加密 """
    if not smali_files:
        return
    # 尝试找到一个含字符串常量的 Smali 文件
    selected_smali = random.choice(smali_files)

    with open(selected_smali, 'r') as file:
        lines = file.readlines()

    # 找到字符串常量
    for i, line in enumerate(lines):
        if line.strip().startswith('const-string'):
            parts = line.strip().split(' ', 2)
            if len(parts) == 3 and '"' in parts[2]:
                # 提取原字符串
                original_str = parts[2].strip('"')
                if len(original_str) > 0:
                    # 进行 Base64 编码
                    encoded_str = base64.b64encode(original_str.encode()).decode()
                    # 构建新的 const-string 行
                    new_line = f'{parts[0]} {parts[1]} "{encoded_str}"\n'
                    lines[i] = new_line
                    print(f"Encoded string at line {i} in {selected_smali}")

                    # 在适当位置添加解码逻辑
                    decoder_line = f'   invoke-static {{{parts[1]}}} Landroid/util/Base64;->decode(Ljava/lang/String;I)[B\n'
                    lines.insert(i+1, decoder_line)
                    decode_line = f'    move-result-object {parts[1]}\n'
                    lines.insert(i+2, decode_line)
                    decode_line = f'    new-instance {parts[1]} Ljava/lang/String;\n'
                    lines.insert(i+3, decode_line)
                    decode_line = f'    invoke-direct {{{parts[1]}, v0}}, Ljava/lang/String;-><init>([B)V\n'
                    lines.insert(i+4, decode_line)
                    break

    # 写回修改后的 Smali 文件
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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reEncode.apk'

    # 收集所有类的标识符
    print("Collecting smali files...")
    smali_files = collect_smali_files(os.path.join(output_folder, 'smali'))

    # 数据加密
    print("Data encoding a random smali file...")
    encode_string(smali_files)

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
