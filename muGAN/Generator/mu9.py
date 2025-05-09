"""
    Mu9-Reflection
    实现 Android 应用的反射调用，通常涉及以下几个步骤：
        1. 解包 APK 文件 --- Apktool
        2. 遍历 smali 文件
        3. 随机选择一个 Smali 文件和其中的一个方法
        4. 修改 Smali 代码以使用反射调用该方法
        5. 重新打包 APK --- Apktool
        6. 对 APK 文件进行签名 --- apksigner
"""
import os
import random

from Generator import set_path, mu1
from Generator.mu7 import collect_smali_files


def reflect_method(smali_files, smali_path):
    """ 随机选择并使用反射调用一个方法 """
    if not smali_files:
        return

    while smali_files:
        # 随机选择一个 Smali 文件
        selected_smali = random.choice(smali_files)
        smali_files.remove(selected_smali)
        print("selected_res: " + selected_smali)

        with open(selected_smali, 'r') as file:
            lines = file.readlines()

        method_start_indices = [i for i, line in enumerate(lines) if line.startswith('.method')]
        method_end_indices = [i for i, line in enumerate(lines) if line.startswith('.end method')]

        if len(method_start_indices) > 0:
            # 随机选择一个方法
            m_index = random.choice(range(len(method_start_indices)))
            m_start, m_end = method_start_indices[m_index], method_end_indices[m_index]
            method_signature_parts = lines[m_start].strip().split()
            method_name = method_signature_parts[-1].split('(')[0]
            print("method_name: " + method_name)

            # 添加反射调用逻辑
            class_path = 'L' + selected_smali[len(smali_path) + len('/smali/'):].replace('\\', '/').replace('.smali', '').replace('/', '/')
            reflect_lines = [
                f'    const-class v0, L{class_path};\n',
                f'    const-string v1, "{method_name}"\n',
                f'    invoke-virtual {{v0, v1}}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;\n',
                f'    move-result-object v0\n',
                f'    const/4 v1, 0x0\n',
                f'    new-array v1, v1, [Ljava/lang/Object;\n',
                f'    invoke-virtual {{v0, v2, v1}}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;\n'
            ]
            lines[m_end:m_end] = reflect_lines

            # 写回修改后的 Smali 文件
            with open(selected_smali, 'w') as file:
                file.writelines(lines)

            print(f"Reflection code in {selected_smali}")
            return


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
    final_signed_apk = apk_name.split('.')[0] + '_' + 'reflection.apk'

    # 收集所有类的标识符
    print("Collecting smali files...")
    smali_files = collect_smali_files(os.path.join(output_folder, 'smali'))

    # 反射调用
    print("Reflecting a random smali file...")
    reflect_method(smali_files, os.path.join(output_folder, 'smali'))

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
